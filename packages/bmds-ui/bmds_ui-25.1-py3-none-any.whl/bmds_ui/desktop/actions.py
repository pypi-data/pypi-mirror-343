import json
import os
import platform
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from pathlib import Path
from threading import Thread
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen
from webbrowser import open_new_tab
from wsgiref.simple_server import WSGIServer, make_server

import django
from django.conf import settings
from django.core.management import call_command
from django.template import Context, Template
from django.template.engine import Engine
from packaging.version import Version, parse
from rich.console import Console
from whitenoise import WhiteNoise

from .. import __version__
from ..main.settings import desktop
from .config import Database, DesktopConfig, get_app_home, get_version_path
from .log import log, stream

PRERELEASE_URL = "https://gitlab.epa.gov/api/v4/projects/1508/packages/pypi/simple"


def sync_persistent_data():
    """Sync persistent data to database and static file path.

    We do this every time a database is created or an application starts, to make sure application
    state is consistent with files.
    """
    call_command("collectstatic", interactive=False, verbosity=3, stdout=stream, stderr=stream)
    call_command("migrate", interactive=False, verbosity=3, stdout=stream, stderr=stream)


def setup_django_environment(db: Database):
    """Set the active django database to the current path and setup the database."""
    app_home = get_app_home()

    desktop.DATABASES["default"]["NAME"] = str(db.path)

    version = get_version_path(__version__)
    public_data_root = app_home / "public" / version
    logs_path = app_home / "logs" / version

    public_data_root.mkdir(exist_ok=True, parents=False)
    logs_path.mkdir(exist_ok=True, parents=False)

    desktop.PUBLIC_DATA_ROOT = public_data_root
    desktop.STATIC_ROOT = public_data_root / "static"
    desktop.MEDIA_ROOT = public_data_root / "media"

    desktop.LOGS_PATH = logs_path
    desktop.LOGGING = desktop.setup_logging(logs_path)

    django.setup()


def create_django_db(db: Database):
    log.info(f"Creating {db}")
    setup_django_environment(db)
    sync_persistent_data()
    log.info(f"Creation successful {db}")


class AppThread(Thread):
    def __init__(self, config: DesktopConfig, db: Database, **kw):
        self.server: WSGIServer | None = None
        self.config = config
        self.db = db
        super().__init__(**kw)

    def _shutdown(self):
        # stop server from another thread to prevent deadlocks
        def _func(server: WSGIServer):
            server.shutdown()

        log.info("Stopping web application...")
        thread = Thread(target=_func, args=(self.server,))
        thread.start()
        log.info("Web application stopped")

    def run(self):
        setup_django_environment(self.db)
        sync_persistent_data()
        from ..main.wsgi import application

        with redirect_stdout(stream), redirect_stderr(stream):
            app = WhiteNoise(application, root=settings.PUBLIC_DATA_ROOT)
            self.server = make_server(self.config.server.host, self.config.server.port, app)
            url = f"http://{self.config.server.host}:{self.config.server.port}"
            log.info(f"Starting {url}")
            if not settings.IS_TESTING:
                open_new_tab(url)
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                log.info(f"Stopping {url}")
            finally:
                call_command("vacuum_db", stdout=stream, stderr=stream)
                self._shutdown()

    def stop(self):
        log.info("Stopping server")
        if self.server is not None:
            self._shutdown()


class AppRunner:
    def __init__(self):
        self.thread: AppThread | None = None

    def start(self, config: DesktopConfig, db: Database):
        if self.thread is None:
            log.info("Searching for free ports")
            config.server.find_free_port()
            log.info(f"Free port found: {config.server.port}")
            config.server.wait_till_free()
            log.info(f"Starting application on {config.server.web_address}")
            self.thread = AppThread(config=config, db=db, daemon=True)
            self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread = None


def get_latest_version(package: str) -> tuple[datetime, Version]:
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        resp = urlopen(url, timeout=5)  # noqa: S310
    except URLError as err:
        parsed = urlparse(url)
        raise ValueError(
            f"Could not check latest version; unable to reach {parsed.scheme}://{parsed.netloc}."
        ) from err
    data = json.loads(resp.read().decode("utf-8"))
    latest_str = list(data["releases"].keys())[-1]
    upload_time = data["releases"][latest_str][0]["upload_time"]
    return datetime.fromisoformat(upload_time), parse(latest_str)


def get_installed_version() -> Version:
    return parse(__version__)


def get_version_message(current: Version, latest: Version, latest_date: datetime) -> str:
    if latest == current:
        return (
            f"You have the latest version installed, {latest} (released {latest_date:%b %d, %Y})."
        )
    elif current < latest:
        return f"There is a newer version available, {latest} (released {latest_date:%b %d, %Y})."
    elif current > latest:
        return f"You have a newer version than what's currently available, {latest} (released {latest_date:%b %d, %Y})."
    raise ValueError("Cannot compare versions")


def show_version():
    """Show the version for BMDS Desktop"""
    console = Console()
    console.print(__version__)


def render_template(template_text: str, context: dict) -> str:
    template = Template(template_text, engine=Engine())
    return template.render(Context(context))


def get_activate_script() -> tuple[str, str]:
    """Try to determine how to activate the environment.

    First check if we're in a python virtual environment with an activate script, next try to
    determine if we're in a conda  environment. If neither, return unknown.

    Returns:
        tuple[str, str]: (environment_type {venv, conda, unknown}, path/name)
    """
    python_path = Path(sys.executable)
    bin_path = python_path.parent
    if (bin_path / "activate").exists():
        return "venv", str(bin_path / "activate")
    elif (bin_path / "activate.bat").exists():
        return "venv", str(bin_path / "activate.bat")
    elif "CONDA_PREFIX" in os.environ and Path(os.environ["CONDA_PREFIX"]).exists():
        return "conda", Path(os.environ["CONDA_PREFIX"]).name
    else:
        return "unknown", ""


def write_startup_script(template: str) -> str:
    python_path = Path(sys.executable)
    env_type, env = get_activate_script()
    show_prerelease = get_installed_version().is_prerelease
    return render_template(
        template,
        {
            "prerelease_url": PRERELEASE_URL,
            "show_prerelease": show_prerelease,
            "python_path": python_path,
            "env_type": env_type,
            "env": env,
        },
    )


def create_shortcut(no_input: bool = False):
    shortcut_path = Path(os.curdir).resolve() / "bmds-desktop"
    shortcut_path.mkdir(exist_ok=True)
    system = platform.system()
    match system:
        case "Windows":
            shortcut = shortcut_path / "bmds-desktop-manager.bat"
            template = (Path(__file__).parent / "templates/manager-bat.txt").read_text()
            script = write_startup_script(template)
            shortcut.write_text(script)
        case "Darwin" | "Linux" | _:
            shortcut = shortcut_path / "bmds-desktop-manager.sh"
            template = (Path(__file__).parent / "templates/manager-sh.txt").read_text()
            script = write_startup_script(template)
            shortcut.touch(mode=0o755, exist_ok=True)
            shortcut.write_text(script)

    console = Console()
    console.print("BMDS Desktop Manager Created:", style="magenta")
    console.print("-----------------------------", style="magenta")
    console.print(shortcut, style="cyan")
    console.print("\nOpening this file will start BMDS Desktop.")
    console.print("You can move this file or create a shortcut to it.\n")

    if not no_input:  # pragma: no cover
        resp = console.input(
            f'Would you like to open the folder to view "{shortcut.name}"? ([cyan]y/n[/cyan])  '
        )
        if resp.lower()[0] == "y":
            match system:
                case "Windows":
                    os.startfile(str(shortcut_path))  # noqa: S606
                case "Darwin":
                    subprocess.run(["open", str(shortcut_path)])  # noqa: S603, S607
                case "Linux" | _:
                    console.print("Sorry, you'll have to open the folder manually.")
