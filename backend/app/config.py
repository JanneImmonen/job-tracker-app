import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[1] / "data" / "job_tracker.db"


@dataclass(frozen=True)
class AppConfig:
    app_env: str
    database_path: Path


def load_config() -> AppConfig:
    app_env = os.getenv("APP_ENV", "development")
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return AppConfig(app_env=app_env, database_path=DEFAULT_DATABASE_PATH)

    sqlite_prefix = "sqlite:///"
    if not database_url.startswith(sqlite_prefix):
        raise ValueError("Only sqlite:/// DATABASE_URL values are currently supported")

    raw_path = unquote(database_url[len(sqlite_prefix) :])
    database_path = Path(raw_path).expanduser()
    if not database_path.is_absolute():
        database_path = (Path.cwd() / database_path).resolve()

    return AppConfig(app_env=app_env, database_path=database_path)
