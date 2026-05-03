import configparser
from app_paths import UI_STATE_PATH

def load_ui_state():
    cfg = configparser.ConfigParser()
    cfg.optionxform = str

    if UI_STATE_PATH.is_file():
        cfg.read(UI_STATE_PATH)
    else:
        cfg["ui"] = {
            "recent_images": "",
            "last_title": "",
            "auto_open_png": "yes",
        }

        with open(UI_STATE_PATH, "w", encoding="utf-8") as f:
            cfg.write(f)

    return cfg


def save_ui_state(cfg):
    with open(UI_STATE_PATH, "w", encoding="utf-8") as f:
        cfg.write(f)