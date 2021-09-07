from pathlib import Path

from dynaconf import Dynaconf


PROJECT_ROOT = Path(__file__).parents[2]
PACKAGE_ROOT = Path(__file__).parents[1]

# Type alias to use throughout the project codebase.
Settings = Dynaconf

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load this files in the order.
settings = Dynaconf(
    envvar_prefix="FASTAPI_DEMO",
    settings_files=['settings.toml', '.secrets.toml'],
)


def get_settings() -> Settings:
    return settings
