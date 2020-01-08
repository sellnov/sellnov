import os
import sys
from importlib import metadata
from pathlib import Path


def extend_sys_path():
    PROJECT_DIR = os.path.join(os.path.dirname(__file__))
    APPS_DIR = os.path.join(PROJECT_DIR, "..", "apps")
    sys.path.insert(0, APPS_DIR)

    PLUGINS_DIR = os.getenv("SELLNOV_PLUGINS_DIR")
    if PLUGINS_DIR:
        p = Path(PLUGINS_DIR).expanduser()
        if not p.is_absolute():
            p = Path.cwd() / p
            if p.exists():
                sys.path.insert(0, str(p))
            else:
                raise ValueError(f"SELLNOV_PLUGINS_DIR does not exists: {p}")


def discover_apps():
    try:
        eps = metadata.entry_points(group="sellnov.plugins")
    except TypeError:
        # Python <3.10 compat
        eps = metadata.entry_points().get("sellnov.plugins", [])
    return [ep.value for ep in eps]
