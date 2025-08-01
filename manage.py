#!/usr/bin/env python
from pathlib import Path

import django
import environ
from django.conf import settings


def init_django() -> None:
    """Initialize Django.

    This function configures the Django settings to use an SQLite3
    database and the `sqlitedb` app. If the settings have already been
    configured, this function does nothing.
    """
    env = environ.Env()
    base_dir = Path(__file__).resolve().parent
    environ.Env.read_env(Path(base_dir, ".env"))

    if settings.configured:
        return
    project_key = env.str("PROJECT_KEY")
    default_cache_url = f"locmemcache://{project_key}?TIMEOUT=86400&KEY_PREFIX=url_bypass"
    settings.configure(
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        INSTALLED_APPS=[
            "sqlitedb",
        ],
        DATABASES={"default": env.db("DATABASE_URL")},
        CACHES={"default": env.cache("CACHE_URL", default=default_cache_url)},
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
