from pathlib import Path
import os
import sys

APP_NAME = "OXRT-StatPlot"

def get_portable_base_dir():
    """
    Real EXE location for Nuitka onefile/standalone.
    """

    if "__compiled__" in globals():
        return Path(__compiled__.containing_dir)

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


def get_appdata_dir():
    """
    Portable-first persistent storage.
    """

    portable_dir = get_portable_base_dir() / f"{APP_NAME}_Data"

    try:
        portable_dir.mkdir(parents=True, exist_ok=True)

        test_file = portable_dir / ".write_test"
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink()

        return portable_dir

    except Exception:
        pass

    fallback = Path(os.getenv("LOCALAPPDATA")) / APP_NAME
    fallback.mkdir(parents=True, exist_ok=True)

    return fallback


APPDATA_DIR = get_appdata_dir()

CONFIG_PATH = APPDATA_DIR / "config.ini"
UI_STATE_PATH = APPDATA_DIR / "ui_state.ini"
LOG_PATH = APPDATA_DIR / "engine.log"
RESULTS_DIR = APPDATA_DIR / "Results"

RESULTS_DIR.mkdir(exist_ok=True)


# ============================================================
# BUNDLED RESOURCES
# ============================================================

def resource_path(relative_path):
    """
    Locate bundled assets for:
    - development
    - Nuitka
    - PyInstaller
    """

    if getattr(sys, "frozen", False):
        base = Path(sys.argv[0]).resolve().parent
    else:
        base = Path(__file__).resolve().parent

    return base / relative_path