r"""
  __  ____  ____  __ _    _  _  ____            ____  ____  __  ____  
 /  \(  _ \(  __)(  ( \  ( \/ )(  _ \          / ___)(_  _)/ _\(_  _) 
(  O )) __/ ) _) /    /   )  (  )   /          \___ \  )( /    \ )(   
 \__/(__)  (____)\_)__)  (_/\_)(__\_)          (____/ (__)\_/\_/(__)  
 ____  __    __   __    __ _  __  ____          ____  __     __  ____ 
(_  _)/  \  /  \ (  )  (  / )(  )(_  _)        (  _ \(  )   /  \(_  _)
  )( (  O )(  O )/ (_/\ )  (  )(   )(           ) __// (_/\(  O ) )(  
 (__) \__/  \__/ \____/(__\_)(__) (__)         (__)  \____/ \__/ (__) 

OXRT-StatPlot
-------------
Author: 75Vette / The Beast
Date: 25 April 2026
Version: 0.9.0

This script is designed specifically for visualizing FPS and performance
metrics from OpenXR Toolkit performance logs (.csv files).

FEATURES:
- Automatically detects all CSV files in the current folder (newest first).
- User selects how many files to plot (1–4).
- User chooses overlay mode, split mode, or frametime distribution:
    * Overlay: all FPS lines on one plot.
    * Split: 1, 2, 3, or 4 subplots (each with FPS + CPU + GPU).
    * Frametime Distribution: percentage vs frametime (ms), 0–20 ms, with Hz guides.
- FPS axis is scaled based on VR headset refresh rate:
    * User chooses 72, 80, 90, 120, 144 Hz, or full range.
    * FPS range = (refresh - 30) to (refresh + 10), with a minimum floor of 42.
    * Full range option = 50–150.
- CPU App, CPU Render, and GPU timings plotted on right secondary axis.
- CPU/GPU timings converted from microseconds to milliseconds.
- Neon color palette on a dark theme.
- True 4K output (3840×2160) or user-selectable lower resolutions.
- Unified smoothing system (None / Light / Medium / Heavy).
- Auto-open PNG after saving (Windows).

DEPENDENCIES:
Install required Python packages with:

    python -m pip install pandas matplotlib

USAGE:
Place this script in the same folder as your CSV logs and run:

    python OXRT-StatPlot-0.8.5.py

The script will guide you interactively.


CHANGELOG
---------

0.3 — VRAM removal + right‑axis redesign
----------------------------------------
Removed:
    - VRAM axis
    - VRAM line
    - VRAM autoscale
    - VRAM color

Changed:
    - Right axis fixed at 0–60 ms
    - FPS axis unchanged (refresh‑rate rule)
    - CPU App, CPU Render, GPU share the right axis
    - Removed twin‑left‑axis hacks

Added:
    - Horizontal dotted ms lines for 72/80/90/120/144 Hz
    - Labels for each dotted line
    - Cleaner subplot layout


0.4 — Automation + neon theme + 4K + VR‑correct scaling
--------------------------------------------------------
- AUTO refresh‑rate detection using VR‑correct rule
- Per‑subplot FPS scaling
- Overlay fallback logic
- 5‑second AUTO default
- Right axis fixed at 0–60 ms
- Dotted ms guide lines for 72/80/90/120/144 Hz
- VRAM removed
- Neon dark theme
- 4K output
- Clean, documented code


0.5 — Stability + correct AUTO detection + no OS hacks
--------------------------------------------------------
- AUTO refresh‑rate detection using 95th percentile FPS
- AUTO is default (press Enter)
- No new terminal windows
- No crashes
- Split mode = per‑subplot FPS scaling
- Overlay mode = fallback to 50–150 if refresh rates differ
- Right axis fixed at 0–60 ms
- Dotted ms guide lines
- VRAM removed
- 4K neon‑dark theme
- Clean, readable code
- Crash‑guard wrapper


0.6 — Correct AUTO detection + correct scaling
-----------------------------------------------
- Correct AUTO detection using dominant FPS cluster
- Correct scaling (refresh − 30, refresh + 10)
- No more mis‑detections
- No more percentile logic
- No more false 120/144 classifications
- Fully stable split/overlay behavior


0.65 — Legend behavior fixes
-----------------------------
Overlay mode:
    - One entry per CSV
    - Neon colors (yellow/cyan/green/magenta)
    - Upper‑left placement

Split mode:
    - FPS (yellow)
    - CPU App (pink)
    - CPU Render (purple)
    - GPU (green)
    - Upper‑right placement


0.66 — Improved readability (ms scale + Hz guides)
---------------------------------------------------
- CPU/GPU ms scale changed to 0–30 ms
- Grey Hz guide lines improved:
    * Lighter grey
    * Thicker
    * More readable text
    * Bold where possible
    * Increased alpha


0.67 — Title/menu improvements + spacing fixes
-----------------------------------------------
- Locale‑aware default title
- New title prompt
- New plot mode menu
- Subplot titles: filename (120 Hz detected)
- Improved spacing to reduce title collisions


0.68 — CSV title inside graph + smoothing + legend overhaul
------------------------------------------------------------
- CSV title moved inside graph, left‑aligned
- Legend box doubled in size
- CPU/GPU ms scale changed to 0–20 ms
- Added smoothing options:
    * Smoothed FPS? Y/N
    * Smoother frametimes? Y/N
- Smoothing style C:
    * Raw lines faint (alpha=0.25)
    * Smoothed lines overlaid (alpha=1.0)
- Final spacing fix (manual subplots_adjust)


0.69 — Header cleanup + metadata + locale fix
-----------------------------------------------
- Removed “‑0.2.py” from header
- Added metadata block (Author, Date, Version)
- Updated locale handling to avoid Python 3.15 deprecation warnings


0.7.0 — Histogram mode + resolution selector + auto-open + menu redesign
------------------------------------------------------------------------
Added:
    - Frametime histogram mode:
        * Split: one histogram per CSV (CPU App + GPU)
        * Overlay: all histograms combined, per-file colour pairs
    - Output resolution selector:
        * 4K (3840×2160) [default]
        * 1440p (2560×1440)
        * 1080p (1920×1080)
    - Auto-open PNG after saving (Windows only)
    - Full ANSI-colour menu redesign (cyan headers, yellow labels, green hotkeys)

Changed:
    - Plot mode menu updated to include histogram options
    - Header version bumped to 0.7.0


0.8.0 — Frametime Distribution mode (percentage vs ms)
------------------------------------------------------
Replaced:
    - Removed histogram mode (split + overlay).

Added:
    - Frametime Distribution mode:
        * Y-axis: Percentage of total frames per frametime bin.
        * X-axis: Frametime (ms), fixed 0–20 ms.
        * Bin resolution: 0.1 ms.
    - Split mode:
        * One frametime distribution line per CSV, using GPU green.
    - Overlay mode:
        * All frametime distributions on one plot, using NEON_FPS_COLORS.
    - Vertical Hz guide lines:
        * 72, 80, 90, 120, 144 Hz converted to ms and drawn as vertical lines.
    - Changelog preserved; version bumped to 0.8.0.
    

0.8.1 — Layout tightening + smoothing defaults
----------------------------------------------
Changed:
    - Reduced external padding around all plots for larger usable area.
    - Updated subplots_adjust() margins for tighter layout.
    - Smoothing (FPS + frametime) now defaults to YES.

Fixed:
    - Overlay distribution title now placed inside plot area.
    - FPS overlay X-axis now correctly spans full duration of all CSVs.

0.8.2 — Adjustable smoothing levels
-----------------------------------
Added:
    - New smoothing level selector:
        * Light (8 samples)
        * Medium (20 samples) [Default]
        * Heavy (40 samples)
    - Smoothing level applies to:
        * FPS
        * CPU App frametime
        * CPU Render frametime
        * GPU frametime

Changed:
    - Smoothing defaults remain enabled (Y) but now user‑selectable.

0.8.3 — Unified smoothing system
--------------------------------
Replaced separate FPS/frametime smoothing prompts with a single smoothing menu:
    None (0), Light (8), Medium (20) [Default], Heavy (40).
Smoothing now applies uniformly across all metrics.
Removed redundant smoothing flags and simplified smoothing logic.

0.8.4 — QoL improvements before packaging
-----------------------------------------
Added:
    - ASCII art banner + version header printed at startup.
    - Automatic detection of OpenXR Toolkit stats directory using USERPROFILE.
    - User prompt for stats path if default directory is missing.
    - PNG output folder: "OXRT StatPlot Results" (auto-created).

Changed:
    - PNG filename format:
        "OXRT StatPlot dd-Mmm-yy - hhmm - {title}.png"
      (spaces instead of underscores, human-readable).

0.8.5 — Config system, console sizing, menu reordering
------------------------------------------------------
Added:
    - config.ini next to the script/exe with full comments and defaults.
    - Persistent stats_dir and output_dir paths with "auto" behaviour.
    - Default resolution, smoothing, refresh rate, plot mode, and title mode in config.
    - Console size control via config (default 120×90).
    - Option to disable ASCII art and auto-open PNG via config.

Changed:
    - Startup header compacted into a single metadata line.
    - Intro line shown immediately after header.
    - Menu order: count → plot mode → file selection → refresh → resolution → smoothing → title.
    - Two-column layouts for refresh, resolution, and smoothing menus.

0.8.6 — Coloured ASCII Art, Exit Menu
------------------------------------------------------
Added:
    - Exit menu

Changed:
    - Colour to ASCII art
    
0.9.0 — Package ready for EXE
------------------------------------------------------
Changed:
    - Minor bug fixes to prepare for EXE package.
"""

# ======================================================================
#  IMPORTS
# ======================================================================

import os
import sys
import locale
import configparser
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("dark_background")

# ======================================================================
#  CONFIG TEMPLATE
# ======================================================================

CONFIG_TEMPLATE = r"""# ============================================================
#  OXRT-StatPlot Configuration File
#  Delete this file at any time to restore factory defaults.
# ============================================================

[paths]
# Path to your OpenXR Toolkit stats directory.
# Use "auto" to let the tool detect it automatically.
stats_dir = {stats_dir}

# Where PNGs should be saved.
# Use "auto" to save into "OXRT StatPlot Results" next to the exe/script.
output_dir = {output_dir}


[defaults]
# Default output resolution:
#   4k, 1440p, 1080p
resolution = {resolution}

# Default smoothing level:
#   none, light, medium, heavy
smoothing = {smoothing}

# Default refresh rate:
#   auto, 72, 80, 90, 120, 144, full
refresh_rate = {refresh_rate}

# Default plot mode:
#   split, overlay, ft_split, ft_overlay
plot_mode = {plot_mode}

# Title behaviour:
#   default  = auto-generated title
#   none     = no title
#   manual   = always ask user
title_mode = {title_mode}

# Show ASCII art banner on startup (yes/no)
show_ascii_art = {show_ascii_art}

# Automatically open PNG after saving (yes/no)
auto_open_png = {auto_open_png}

# Verbose mode prints extra debug info (yes/no)
verbose = {verbose}
"""

# ======================================================================
#  CONFIG HANDLING
# ======================================================================

def get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_config_path():
    return os.path.join(get_base_dir(), "config.ini")

def load_config():
    """
    Load config.ini if present; if missing, create one with factory defaults.
    Returns a ConfigParser instance.
    """
    base_dir = get_base_dir()
    config_path = get_config_path()

    # Factory defaults
    defaults = {
        "paths": {
            "stats_dir": "auto",
            "output_dir": "auto",
        },
        "defaults": {
            "resolution": "4k",
            "smoothing": "medium",
            "refresh_rate": "auto",
            "plot_mode": "split",
            "title_mode": "default",
        },
        "ui": {
            "console_width": "120",
            "console_height": "90",
            "show_ascii_art": "yes",
            "auto_open_png": "yes",
            "verbose": "no",
        },
    }

    config = configparser.ConfigParser()
    if os.path.isfile(config_path):
        config.read(config_path)
    else:
        # Create a fresh config.ini with defaults
        write_config_from_values(defaults)
        config.read(config_path)

    # Ensure all sections/keys exist (non-destructive)
    changed = False
    for section, values in defaults.items():
        if not config.has_section(section):
            config.add_section(section)
            changed = True
        for key, val in values.items():
            if not config.has_option(section, key):
                config.set(section, key, val)
                changed = True

    if changed:
        save_config(config)

    return config

def write_config_from_values(values):
    """
    Write config.ini using CONFIG_TEMPLATE and a dict-of-dicts 'values'.
    This preserves comments while allowing updated values.
    """
    base_dir = get_base_dir()
    config_path = get_config_path()

    paths = values.get("paths", {})
    defaults = values.get("defaults", {})
    ui = values.get("ui", {})

    stats_dir = paths.get("stats_dir", "auto")
    output_dir = paths.get("output_dir", "auto")

    resolution = defaults.get("resolution", "4k")
    smoothing = defaults.get("smoothing", "medium")
    refresh_rate = defaults.get("refresh_rate", "auto")
    plot_mode = defaults.get("plot_mode", "split")
    title_mode = defaults.get("title_mode", "default")

    console_width = ui.get("console_width", "120")
    console_height = ui.get("console_height", "90")
    show_ascii_art = ui.get("show_ascii_art", "yes")
    auto_open_png = ui.get("auto_open_png", "yes")
    verbose = ui.get("verbose", "no")

    text = CONFIG_TEMPLATE.format(
        stats_dir=stats_dir,
        output_dir=output_dir,
        resolution=resolution,
        smoothing=smoothing,
        refresh_rate=refresh_rate,
        plot_mode=plot_mode,
        title_mode=title_mode,
        console_width=console_width,
        console_height=console_height,
        show_ascii_art=show_ascii_art,
        auto_open_png=auto_open_png,
        verbose=verbose,
    )

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(text)

def save_config(config):
    """
    Save config.ini while preserving comments by re-emitting CONFIG_TEMPLATE
    with current values from the ConfigParser.
    """
    values = {
        "paths": {
            "stats_dir": config.get("paths", "stats_dir", fallback="auto"),
            "output_dir": config.get("paths", "output_dir", fallback="auto"),
        },
        "defaults": {
            "resolution": config.get("defaults", "resolution", fallback="4k"),
            "smoothing": config.get("defaults", "smoothing", fallback="medium"),
            "refresh_rate": config.get("defaults", "refresh_rate", fallback="auto"),
            "plot_mode": config.get("defaults", "plot_mode", fallback="split"),
            "title_mode": config.get("defaults", "title_mode", fallback="default"),
        },
        "ui": {
            "console_width": config.get("ui", "console_width", fallback="120"),
            "console_height": config.get("ui", "console_height", fallback="90"),
            "show_ascii_art": config.get("ui", "show_ascii_art", fallback="yes"),
            "auto_open_png": config.get("ui", "auto_open_png", fallback="yes"),
            "verbose": config.get("ui", "verbose", fallback="no"),
        },
    }
    write_config_from_values(values)


# ======================================================================
#  ASCII ART HEADER (PRINTED AT STARTUP)  (COLOURED IN 0.8.6)
# ======================================================================

def print_header(show_ascii=True):
    if show_ascii:

        # Line 1
        print(
            f"{C_PURP}  __  ____  ____  __ _      _  _  ____ {C_RESET}"
            f"{C_BLUE}     ____  ____  __  ____  {C_RESET}"
        )

        # Line 2
        print(
            f"{C_PURP} /  \\(  _ \\(  __)(  ( \\    ( \\/ )(  _ \\{C_RESET}"
            f"{C_BLUE}    / ___)(_  _)/ _\\(_  _){C_RESET}"
        )

        # Line 3
        print(
            f"{C_PURP}(  O )) __/ ) _) /    /     )  (  )   /{C_RESET}"
            f"{C_BLUE}    \\___ \\  )( /    \\ )(  {C_RESET}"
        )

        # Line 4
        print(
            f"{C_PURP} \\__/(__)  (____)\\_)__)    (_/\\_)(__\\_){C_RESET}"
            f"{C_BLUE}    (____/ (__)_/\\_/(__) {C_RESET}"
        )

        # Line 5
        print(
            f"{C_PURP} ____  __    __   __    __ _  __  ____ {C_RESET}"
            f"{C_YEL}     ____  __     __  ____ {C_RESET}"
        )

        # Line 6
        print(
            f"{C_PURP}(_  _)/  \\  /  \\ (  )  (  / )(  )(_  _){C_RESET}"
            f"{C_YEL}    (  _ \\(  )   /  \\(_  _){C_RESET}"
        )

        # Line 7
        print(
            f"{C_PURP}  )( (  O )(  O )/ (_/\\ )  (  )(   )(  {C_RESET}"
            f"{C_YEL}     ) __// (_/\\(  O ) )(  {C_RESET}"
        )

        # Line 8
        print(
            f"{C_PURP} (__) \\__/  \\__/ \\____/(__\\_)(__) (__) {C_RESET}"
            f"{C_YEL}    (__)  \\____/ \\__/ (__) {C_RESET}"
        )

    print()
    header = "OXRT-StatPlot 0.9.0         75Vette / The Beast        25 April 2026"
    print(header)
    print("-" * len(header))
    print("This script is designed specifically for visualizing FPS and performance")
    print("metrics from OpenXR Toolkit performance logs (.csv files).\n")



# ======================================================================
#  ANSI COLOUR CONSTANTS
# ======================================================================

C_RESET = "\033[0m"
C_CYAN  = "\033[96m"
C_YEL   = "\033[93m"
C_GRN   = "\033[92m"
C_GREY  = "\033[90m"
# New for 0.8.6
C_PURP = "\033[95m"   # neon purple
C_BLUE = "\033[94m"   # neon blue

FT_OVERLAY_PAIRS = [
    ("#f5f749", "#ffb84d"),   # yellow + orange
    ("#4df2ff", "#0099cc"),   # cyan + deep blue
    ("#7CFF6B", "#2ea043"),   # neon green + dark green
    ("#ff4df2", "#c44dff"),   # neon pink + magenta
]

# ======================================================================
#  COLOR PALETTE
# ======================================================================

NEON_FPS_COLORS = ["#f5f749", "#4df2ff", "#7CFF6B", "#ff4df2", "#ffb84d", "#c44dff"]

COLOR_FPS = "#f5f749"
COLOR_CPU_APP = "#ff4df2"
COLOR_CPU_RENDER = "#c44dff"
COLOR_GPU = "#7CFF6B"
COLOR_GUIDE = "#AAAAAA"

KNOWN_REFRESH_RATES = [72, 80, 90, 120, 144]

# ======================================================================
#  FILE DISCOVERY + SELECTION
# ======================================================================

def list_csv_files():
    files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files

def print_file_list(files):
    print(f"\n{C_CYAN}Available CSV files (newest first):{C_RESET}\n")
    for i, f in enumerate(files, start=1):
        print(f"{C_GRN}{i}{C_RESET}. {C_YEL}{f}{C_RESET}")

def choose_file_count(max_files):
    print(f"\n{C_CYAN}How many logs do you wish to plot? (1–{max_files}){C_RESET}")
    while True:
        try:
            count = int(input("> ").strip())
            if 1 <= count <= max_files:
                return count
            print(f"Enter a number between 1 and {max_files}.")
        except ValueError:
            print("Invalid input.")

def select_files(files, count):
    print_file_list(files)
    print()  # extra spacing before selection prompt
    print(f"{C_CYAN}Select your logs (comma or space separated indices). Example: 1 3 or 1,3{C_RESET}")
    while True:
        raw = input("> ").strip().replace(",", " ")
        try:
            idx = [int(x) for x in raw.split() if x]
            if len(idx) != count:
                print(f"Select exactly {count} files.")
                continue
            if any(i < 1 or i > len(files) for i in idx):
                print("Selection out of range.")
                continue
            break
        except ValueError:
            print("Invalid input.")
    return [files[i - 1] for i in idx]

# Keep original pick_files for backward compatibility (unused in 0.8.5)
def pick_files(files):
    print(f"\n{C_CYAN}Available CSV files (newest first):{C_RESET}\n")
    for i, f in enumerate(files, start=1):
        print(f"{C_GRN}{i}{C_RESET}. {C_YEL}{f}{C_RESET}")

    print(f"\n{C_CYAN}How many files do you want to plot? (1–4){C_RESET}")
    while True:
        try:
            count = int(input("> ").strip())
            if 1 <= count <= 4:
                break
            print("Enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input.")

    print(f"\n{C_CYAN}Enter the file numbers (comma-separated). Example: 1,3{C_RESET}")
    while True:
        raw = input("> ").strip()
        try:
            idx = [int(x) for x in raw.split(",")]
            if len(idx) != count:
                print(f"Select exactly {count} files.")
                continue
            if any(i < 1 or i > len(files) for i in idx):
                print("Selection out of range.")
                continue
            break
        except ValueError:
            print("Invalid input.")

    return [files[i - 1] for i in idx]

# ======================================================================
#  REFRESH RATE HANDLING
# ======================================================================

def auto_detect_refresh_rate(df):
    if "FPS" not in df.columns or df["FPS"].empty:
        return None
    rounded = df["FPS"].round().astype(int)
    counts = rounded.value_counts()
    if counts.empty:
        return None
    dominant = counts.idxmax()
    refresh = min(KNOWN_REFRESH_RATES, key=lambda hz: abs(hz - dominant))
    return refresh

def choose_refresh_rate(default="auto"):
    print(f"\n{C_CYAN}Step 4: Select target refresh rate or allow auto detection per log file:{C_RESET}")

    print(f"{C_GRN}1{C_RESET}. {C_YEL}AUTO (recommended){C_RESET}        "
          f"{C_GRN}5{C_RESET}. {C_YEL}120 Hz{C_RESET}")

    print(f"{C_GRN}2{C_RESET}. {C_YEL}72 Hz{C_RESET}                     "
          f"{C_GRN}6{C_RESET}. {C_YEL}144 Hz{C_RESET}")

    print(f"{C_GRN}3{C_RESET}. {C_YEL}80 Hz{C_RESET}                     "
          f"{C_GRN}7{C_RESET}. {C_YEL}Full range (50–150 Hz){C_RESET}")

    print(f"{C_GRN}4{C_RESET}. {C_YEL}90 Hz{C_RESET}")

    print(f"\nPress ENTER for default: {default.upper()}")

    choice = input("> ").strip()
    if choice == "":
        choice = {
            "auto": "1",
            "72": "2",
            "80": "3",
            "90": "4",
            "120": "5",
            "144": "6",
            "full": "7",
        }.get(default.lower(), "1")

    if choice == "1":
        return "AUTO"

    mapping = {
        "2": 72,
        "3": 80,
        "4": 90,
        "5": 120,
        "6": 144,
        "7": "FULL"
    }
    return mapping.get(choice, "AUTO")

def fps_range_for_refresh(refresh):
    if refresh == "FULL":
        return (50, 150)
    lower = max(42, refresh - 30)
    upper = refresh + 10
    return (lower, upper)

# ======================================================================
#  SMOOTHING OPTION
# ======================================================================

def choose_smoothing_level(default="medium"):
    print(f"\n{C_CYAN}Step 6: Smoothing level (raw results still visible behind):{C_RESET}")
    print(f"{C_GRN}1{C_RESET}. {C_YEL}None (0 samples){C_RESET}        {C_GRN}3{C_RESET}. {C_YEL}Medium (20 samples){C_RESET}")
    print(f"{C_GRN}2{C_RESET}. {C_YEL}Light (8 samples){C_RESET}       {C_GRN}4{C_RESET}. {C_YEL}Heavy (40 samples){C_RESET}")

    default_map = {
        "none": "1",
        "light": "2",
        "medium": "3",
        "heavy": "4",
    }
    default_choice = default_map.get(default.lower(), "3")
    print(f"\nPress ENTER for default: {default.capitalize()}")

    choice = input("> ").strip()
    if choice == "":
        choice = default_choice

    if choice == "1":
        return 0
    if choice == "2":
        return 8
    if choice == "3":
        return 20
    if choice == "4":
        return 40
    return 20

# ======================================================================
#  RESOLUTION SELECTOR
# ======================================================================

def choose_resolution(default="4k"):
    print(f"\n{C_CYAN}Step 5: Select output resolution for plot:{C_RESET}")
    print(f"{C_GRN}1{C_RESET}. {C_YEL}4K  (3840×2160){C_RESET}")
    print(f"{C_GRN}2{C_RESET}. {C_YEL}1440p (2560×1440){C_RESET}")
    print(f"{C_GRN}3{C_RESET}. {C_YEL}1080p (1920×1080){C_RESET}")

    default_map = {
        "4k": "1",
        "1440p": "2",
        "1080p": "3",
    }
    default_choice = default_map.get(default.lower(), "1")
    print(f"\nPress ENTER for default: {default.upper()}")

    choice = input("> ").strip()
    if choice == "":
        choice = default_choice

    if choice == "1":
        return (38.4, 21.6)
    if choice == "2":
        return (25.6, 14.4)
    if choice == "3":
        return (19.2, 10.8)
    return (38.4, 21.6)

# ======================================================================
#  PLOT MODE MENU (UPDATED ORDER)
# ======================================================================

def choose_plot_mode(default="split"):
    print(f"\n{C_CYAN}Step 2: How do you wish to plot them?{C_RESET}")
    print(f"{C_GRN}1{C_RESET}. {C_YEL}Split Plot – FPS + CPU/GPU{C_RESET}")
    print(f"{C_GRN}2{C_RESET}. {C_YEL}Overlay Plot – FPS only{C_RESET}")
    print(f"{C_GRN}3{C_RESET}. {C_YEL}Frametime Distribution (Split – GPU + CPU App + CPU Render){C_RESET}")
    print(f"{C_GRN}4{C_RESET}. {C_YEL}Frametime Distribution (Overlay – GPU + CPU App only){C_RESET}")

    default_map = {
        "split": "1",
        "overlay": "2",
        "ft_split": "3",
        "ft_overlay": "4",
    }
    default_choice = default_map.get(default.lower(), "1")
    print(f"\nPress ENTER for default: {default.replace('_', ' ').title()}")

    choice = input("> ").strip()
    if choice == "":
        choice = default_choice

    if choice == "1":
        return "FPS_SPLIT"
    if choice == "2":
        return "FPS_OVERLAY"
    if choice == "3":
        return "FT_DIST_SPLIT"
    if choice == "4":
        return "FT_DIST_OVERLAY"
    return "FPS_SPLIT"

# ======================================================================
#  USER INPUT HELPERS
# ======================================================================

def ask_yes_no(prompt, default=False):
    default_str = "N" if not default else "Y"
    print(f"\n{C_CYAN}{prompt}{C_RESET} Y/N (Default {default_str}):")
    raw = input("> ").strip().lower()
    if raw == "":
        return default
    if raw.startswith("y"):
        return True
    if raw.startswith("n"):
        return False
    return default

def format_default_title():
    try:
        loc = locale.getlocale()[0] or ""
    except:
        loc = ""
    now = datetime.now()
    if loc.startswith("en_US"):
        date_str = now.strftime("%m/%d/%y")
    else:
        date_str = now.strftime("%d/%m/%y")
    time_str = now.strftime("%H:%M")
    return f"OpenXR Toolkit Stat Plot – {time_str} {date_str}"

def get_title_from_user(title_mode="default"):
    """
    title_mode:
        default -> auto title on ENTER
        none    -> no title
        manual  -> always ask user
    """
    if title_mode == "none":
        return None

    print(f"\n{C_CYAN}Step 7: What would you like to call this plot?{C_RESET}")
    print("Enter: Default title")
    print("0: No title")

    raw = input("> ").strip()
    if raw == "0":
        return None
    if raw == "":
        if title_mode in ("default", "manual"):
            return format_default_title()
        return None
    return raw

# ======================================================================
#  DATA LOADING + PROCESSING
# ======================================================================

def load_and_process(csv_file):
    df = pd.read_csv(csv_file)
    df["time"] = pd.to_datetime(df["time"])
    df["elapsed_min"] = (df["time"] - df["time"].min()).dt.total_seconds() / 60

    df["appCPU_ms"] = df["appCPU (us)"] / 1000.0
    df["renderCPU_ms"] = df["renderCPU (us)"] / 1000.0
    df["appGPU_ms"] = df["appGPU (us)"] / 1000.0

    return df

# ======================================================================
#  GUIDE LINES (FPS + FRAMETIME)
# ======================================================================

def add_ms_guide_lines(ax_right):
    for fps in KNOWN_REFRESH_RATES:
        ms = 1000.0 / fps
        if 0 <= ms <= 20:
            ax_right.axhline(
                ms,
                color="#AAAAAA",
                linestyle=":",
                linewidth=1.4,
                alpha=0.8
            )
            ax_right.text(
                1.0, ms, f"{fps} Hz",
                color="#CCCCCC",
                fontsize=10,
                fontweight="bold",
                alpha=0.9,
                ha="right",
                va="bottom",
                transform=ax_right.get_yaxis_transform()
            )

def add_vertical_hz_lines(ax):
    for hz in KNOWN_REFRESH_RATES:
        ms = 1000.0 / hz
        if 0 <= ms <= 20:
            ax.axvline(
                ms,
                color="#AAAAAA",
                linestyle="--",
                linewidth=1.4,
                alpha=0.8
            )
            ax.text(
                ms, 1.0,
                f"{hz} Hz",
                color="#CCCCCC",
                fontsize=10,
                fontweight="bold",
                alpha=0.9,
                ha="center",
                va="bottom",
                transform=ax.get_xaxis_transform()
            )

# ======================================================================
#  SUBPLOT CREATION (FPS SPLIT MODE)
# ======================================================================

def create_subplot(ax, df, filename, refresh):
    fps_range = fps_range_for_refresh(refresh)
    handles = []

    if "FPS_smooth" in df.columns:
        ax.plot(df["elapsed_min"], df["FPS"], color=COLOR_FPS, alpha=0.25, linewidth=1.0)
        fps_line, = ax.plot(df["elapsed_min"], df["FPS_smooth"],
                            color=COLOR_FPS, alpha=1.0, linewidth=2.0,
                            label="FPS (smoothed)")
    else:
        fps_line, = ax.plot(df["elapsed_min"], df["FPS"],
                            color=COLOR_FPS, linewidth=1.5, label="FPS")

    handles.append(fps_line)

    ax.set_xlabel("Elapsed Time (minutes)")
    ax.set_ylabel("FPS", color=COLOR_FPS)
    ax.tick_params(axis='y', colors=COLOR_FPS)
    ax.grid(True, alpha=0.3)

    ax_r = ax.twinx()

    if "appCPU_ms_smooth" in df.columns:
        ax_r.plot(df["elapsed_min"], df["appCPU_ms"], color=COLOR_CPU_APP, alpha=0.25, linewidth=1.0)
        ax_r.plot(df["elapsed_min"], df["renderCPU_ms"], color=COLOR_CPU_RENDER, alpha=0.25, linewidth=1.0)
        ax_r.plot(df["elapsed_min"], df["appGPU_ms"], color=COLOR_GPU, alpha=0.25, linewidth=1.0)

        cpu_app_line, = ax_r.plot(df["elapsed_min"], df["appCPU_ms_smooth"],
                                  color=COLOR_CPU_APP, alpha=1.0, linewidth=2.0,
                                  label="CPU App (smoothed)")
        cpu_render_line, = ax_r.plot(df["elapsed_min"], df["renderCPU_ms_smooth"],
                                     color=COLOR_CPU_RENDER, alpha=1.0, linewidth=2.0,
                                     label="CPU Render (smoothed)")
        gpu_line, = ax_r.plot(df["elapsed_min"], df["appGPU_ms_smooth"],
                              color=COLOR_GPU, alpha=1.0, linewidth=2.0,
                              label="GPU (smoothed)")
    else:
        cpu_app_line, = ax_r.plot(df["elapsed_min"], df["appCPU_ms"],
                                  color=COLOR_CPU_APP, linewidth=1.5, label="CPU App")
        cpu_render_line, = ax_r.plot(df["elapsed_min"], df["renderCPU_ms"],
                                     color=COLOR_CPU_RENDER, linewidth=1.5, label="CPU Render")
        gpu_line, = ax_r.plot(df["elapsed_min"], df["appGPU_ms"],
                              color=COLOR_GPU, linewidth=1.5, label="GPU")

    handles.extend([cpu_app_line, cpu_render_line, gpu_line])

    ax_r.set_ylabel("CPU/GPU (ms)", color=COLOR_GPU)
    ax_r.tick_params(axis='y', colors=COLOR_GPU)
    ax_r.set_ylim(0, 20)

    add_ms_guide_lines(ax_r)

    ax.set_autoscale_on(False)
    ax.set_ylim(fps_range[0], fps_range[1])

    if isinstance(refresh, int):
        hz_label = f"{refresh} Hz detected"
    else:
        hz_label = "Full range"

    ax.text(
        0.01, 0.98,
        f"{filename} ({hz_label})",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
        color="#DDDDDD"
    )

    ax.legend(
        handles=handles,
        loc="upper right",
        fontsize=14,
        framealpha=0.85,
        borderpad=1.2,
        labelspacing=1.0,
        handlelength=3.0,
        handletextpad=1.0
    )

# ======================================================================
#  FPS OVERLAY MODE
# ======================================================================

def plot_fps_overlay(fig, dfs, selected):
    ax = fig.add_subplot(1, 1, 1)

    detected = []
    for f in selected:
        df = dfs[f]
        hz = auto_detect_refresh_rate(df)
        detected.append(hz if hz else "FULL")

    unique = set(detected)
    if len(unique) == 1 and list(unique)[0] != "FULL":
        refresh = list(unique)[0]
        fps_range = fps_range_for_refresh(refresh)
    else:
        refresh = "FULL"
        fps_range = (50, 150)

    xmin = min(dfs[f]["elapsed_min"].min() for f in selected)
    xmax = max(dfs[f]["elapsed_min"].max() for f in selected)
    ax.set_xlim(xmin, xmax)

    legend_handles = []

    for i, f in enumerate(selected):
        df = dfs[f]
        color = NEON_FPS_COLORS[i % len(NEON_FPS_COLORS)]

        if "FPS_smooth" in df.columns:
            ax.plot(df["elapsed_min"], df["FPS"], color=color, alpha=0.25, linewidth=1.0)
            line, = ax.plot(df["elapsed_min"], df["FPS_smooth"],
                            color=color, alpha=1.0, linewidth=2.0, label=f)
        else:
            line, = ax.plot(df["elapsed_min"], df["FPS"],
                            color=color, linewidth=1.5, label=f)

        legend_handles.append(line)

    ax.set_autoscale_on(False)
    ax.set_ylim(fps_range[0], fps_range[1])
    ax.set_xlabel("Elapsed Time (minutes)")
    ax.set_ylabel("FPS")
    ax.grid(True, alpha=0.3)

    ax.legend(
        handles=legend_handles,
        loc="upper left",
        fontsize=14,
        framealpha=0.85,
        borderpad=1.2,
        labelspacing=1.0,
        handlelength=3.0,
        handletextpad=1.0
    )

    fig.subplots_adjust(
        left=0.02,
        right=0.98,
        top=0.96,
        bottom=0.02,
        hspace=0.08,
        wspace=0.08
    )

# ======================================================================
#  FRAMETIME DISTRIBUTION (0.8.0)
# ======================================================================

def compute_ft_distribution(df):
    ft_gpu = df["appGPU_ms"].values
    ft_app = df["appCPU_ms"].values
    ft_render = df["renderCPU_ms"].values

    mask = lambda x: x[(x >= 0) & (x <= 20)]

    ft_gpu = mask(ft_gpu)
    ft_app = mask(ft_app)
    ft_render = mask(ft_render)

    bins = np.arange(0, 20.0001, 0.1)

    def pct(x):
        counts, edges = np.histogram(x, bins=bins)
        total = counts.sum()
        if total == 0:
            return np.zeros_like(counts, dtype=float)
        return (counts / total) * 100.0

    pct_gpu = pct(ft_gpu)
    pct_app = pct(ft_app)
    pct_render = pct(ft_render)

    centers = (bins[:-1] + bins[1:]) / 2.0
    return centers, pct_gpu, pct_app, pct_render


def plot_ft_dist_split(fig, dfs, selected):
    count = len(selected)
    layout = {1: (1, 1), 2: (2, 1), 3: (2, 2), 4: (2, 2)}[count]
    rows, cols = layout

    for idx, f in enumerate(selected, start=1):
        df = dfs[f]
        centers, pct_gpu, pct_app, pct_render = compute_ft_distribution(df)

        ax = fig.add_subplot(rows, cols, idx)

        ax.plot(centers, pct_gpu, color=COLOR_GPU, linewidth=2.0, label="GPU")
        ax.plot(centers, pct_app, color=COLOR_CPU_APP, linewidth=2.0, label="CPU App")
        ax.plot(centers, pct_render, color=COLOR_CPU_RENDER, linewidth=2.0, label="CPU Render")

        ymax = max(pct_gpu.max(), pct_app.max(), pct_render.max(), 1)
        ax.set_ylim(-0.5, ymax * 1.05)

        ax.set_xlim(0, 20)

        add_vertical_hz_lines(ax)

        ax.set_xlabel("Frametime (ms)")
        ax.set_ylabel("Percentage (%)")

        ax.text(
            0.01, 0.98,
            f"{f}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=12,
            fontweight="bold",
            color="#DDDDDD"
        )

        ax.legend(
            loc="upper right",
            fontsize=14,
            framealpha=0.85,
            borderpad=1.2,
            labelspacing=1.0,
            handlelength=3.0,
            handletextpad=1.0
        )

    fig.subplots_adjust(
        left=0.02,
        right=0.98,
        top=0.96,
        bottom=0.02,
        hspace=0.08,
        wspace=0.08
    )


def plot_ft_dist_overlay(fig, dfs, selected):
    ax = fig.add_subplot(1, 1, 1)

    ymax = 1

    for i, f in enumerate(selected):
        df = dfs[f]
        centers, pct_gpu, pct_app, _ = compute_ft_distribution(df)

        gpu_color, cpu_color = FT_OVERLAY_PAIRS[i % len(FT_OVERLAY_PAIRS)]

        ax.plot(centers, pct_gpu, color=gpu_color, linewidth=2.0, label=f"{f} – GPU")
        ax.plot(centers, pct_app, color=cpu_color, linewidth=2.0, alpha=0.9, label=f"{f} – CPU App")

        ymax = max(ymax, pct_gpu.max(), pct_app.max())

    ax.set_xlim(0, 20)
    ax.set_ylim(-0.5, ymax * 1.05)

    add_vertical_hz_lines(ax)

    ax.set_xlabel("Frametime (ms)")
    ax.set_ylabel("Percentage (%)")
    ax.text(
        0.01, 0.98,
        "Frametime Distribution – Overlay (GPU + CPU App)",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=14,
        fontweight="bold",
        color="#DDDDDD"
    )

    ax.legend(
        loc="upper right",
        fontsize=14,
        framealpha=0.85,
        borderpad=1.2,
        labelspacing=1.0,
        handlelength=3.0,
        handletextpad=1.0
    )

    fig.subplots_adjust(
        left=0.02,
        right=0.98,
        top=0.96,
        bottom=0.02,
        hspace=0.08,
        wspace=0.08
    )

# ======================================================================
#  DEFAULT STATS PATH HELPER
# ======================================================================

def get_default_stats_path():
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        return None
    return os.path.join(
        user_profile,
        "AppData",
        "Local",
        "OpenXR-Toolkit",
        "stats"
    )

# ======================================================================
#  MAIN
# ======================================================================

def main():
    try:
        # Load config and apply console/UI settings
        config = load_config()

        console_width = int(config.get("ui", "console_width", fallback="120"))
        console_height = int(config.get("ui", "console_height", fallback="90"))

        show_ascii = config.get("ui", "show_ascii_art", fallback="yes").lower() == "yes"
        auto_open_png = config.get("ui", "auto_open_png", fallback="yes").lower() == "yes"

        print_header(show_ascii=show_ascii)

        # Resolve stats directory
        stats_dir = config.get("paths", "stats_dir", fallback="auto")
        if stats_dir.lower() == "auto":
            default_stats_path = get_default_stats_path()
            if default_stats_path and os.path.isdir(default_stats_path):
                os.chdir(default_stats_path)
            else:
                print(f"{C_CYAN}OpenXR Toolkit stats folder not found at default location.{C_RESET}")
                print("Please enter the full path to your stats directory:")
                while True:
                    user_path = input("> ").strip().strip('"')
                    if os.path.isdir(user_path):
                        stats_dir = user_path
                        config.set("paths", "stats_dir", stats_dir)
                        save_config(config)
                        os.chdir(stats_dir)
                        break
                    print("Invalid path. Please try again.")
        else:
            if os.path.isdir(stats_dir):
                os.chdir(stats_dir)
            else:
                print(f"{C_CYAN}Configured stats_dir is invalid.{C_RESET}")
                print("Please enter the full path to your stats directory:")
                while True:
                    user_path = input("> ").strip().strip('"')
                    if os.path.isdir(user_path):
                        stats_dir = user_path
                        config.set("paths", "stats_dir", stats_dir)
                        save_config(config)
                        os.chdir(stats_dir)
                        break
                    print("Invalid path. Please try again.")

        files = list_csv_files()
        if not files:
            print("No CSV files found.")
            return

        # Step 1: How many logs
        max_files = min(4, len(files))
        count = choose_file_count(max_files)

        # Step 2: Plot mode (from config default)
        plot_mode_default = config.get("defaults", "plot_mode", fallback="split")
        print()  # spacing before plot mode menu
        mode = choose_plot_mode(default=plot_mode_default)

        # Step 3: Select logs
        print()  # spacing before file selection
        selected = select_files(files, count)

        # Step 4: Refresh rate (from config default)
        refresh_default = config.get("defaults", "refresh_rate", fallback="auto")
        print()  # spacing before refresh menu
        refresh_choice = choose_refresh_rate(default=refresh_default)

        # Step 5: Resolution (from config default)
        resolution_default = config.get("defaults", "resolution", fallback="4k")
        print()  # spacing before resolution menu
        resolution = choose_resolution(default=resolution_default)

        # Step 6: Smoothing (from config default)
        smoothing_default = config.get("defaults", "smoothing", fallback="medium")
        print()  # spacing before smoothing menu
        window = choose_smoothing_level(default=smoothing_default)

        # Step 7: Title (from config default)
        title_mode = config.get("defaults", "title_mode", fallback="default")
        print()  # spacing before title prompt
        title = get_title_from_user(title_mode=title_mode)

        # New human-readable filename format
        now = datetime.now()
        date_str = now.strftime("%d-%b-%y")   # 25-Apr-26
        time_str = now.strftime("%H%M")       # 1842

        safe_title = title or "No Title"
        safe_title = "".join(
            c for c in safe_title if c.isalnum() or c in (" ", "-")
        )

        output_name = f"OXRT StatPlot {date_str} - {time_str} - {safe_title}.png"

        # Resolve output directory
        output_dir_cfg = config.get("paths", "output_dir", fallback="auto")
        if output_dir_cfg.lower() == "auto":
            output_dir = os.path.join(get_base_dir(), "OXRT StatPlot Results")
        else:
            output_dir = output_dir_cfg

        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception:
                print(f"{C_CYAN}Configured output_dir is invalid or not creatable.{C_RESET}")
                print("Please enter a valid output directory path:")
                while True:
                    user_path = input("> ").strip().strip('"')
                    try:
                        os.makedirs(user_path, exist_ok=True)
                        output_dir = user_path
                        config.set("paths", "output_dir", output_dir)
                        save_config(config)
                        break
                    except Exception:
                        print("Could not create that directory. Please try again.")

        output_path = os.path.join(output_dir, output_name)

        fig = plt.figure(figsize=resolution, dpi=100)

        dfs = {f: load_and_process(f) for f in selected}

        detected = {}
        if refresh_choice == "AUTO":
            for f, df in dfs.items():
                hz = auto_detect_refresh_rate(df)
                detected[f] = hz if hz else "FULL"
        else:
            for f in selected:
                detected[f] = refresh_choice

        # Apply smoothing if window > 0
        for f, df in dfs.items():
            if window > 0:
                df["FPS_smooth"] = df["FPS"].rolling(
                    window=window, center=True, min_periods=1
                ).mean()
                df["appCPU_ms_smooth"] = df["appCPU_ms"].rolling(
                    window=window, center=True, min_periods=1
                ).mean()
                df["renderCPU_ms_smooth"] = df["renderCPU_ms"].rolling(
                    window=window, center=True, min_periods=1
                ).mean()
                df["appGPU_ms_smooth"] = df["appGPU_ms"].rolling(
                    window=window, center=True, min_periods=1
                ).mean()

        # ==================================================================
        #  FRAMETIME DISTRIBUTION (0.8.0)
        # ==================================================================
        if mode == "FT_DIST_SPLIT":
            plot_ft_dist_split(fig, dfs, selected)
            if title is not None:
                fig.suptitle(title, fontsize=24)
            plt.savefig(output_path)
            if auto_open_png:
                try:
                    os.startfile(output_path)
                except:
                    pass
            print(f"\nSaved {output_path}")
            print("\nWhat next?")
            print("1. Run again")
            print("2. Exit")

            choice = input("> ").strip()
            if choice == "1":
                main()
            return


        if mode == "FT_DIST_OVERLAY":
            plot_ft_dist_overlay(fig, dfs, selected)
            if title is not None:
                fig.suptitle(title, fontsize=24)
            plt.savefig(output_path)
            if auto_open_png:
                try:
                    os.startfile(output_path)
                except:
                    pass
            print(f"\nSaved {output_path}")
            print("\nWhat next?")
            print("1. Run again")
            print("2. Exit")

            choice = input("> ").strip()
            if choice == "1":
                main()
            return


        # ==================================================================
        #  FPS SPLIT MODE
        # ==================================================================
        if mode == "FPS_SPLIT":
            count = len(selected)
            layout = {1: (1, 1), 2: (2, 1), 3: (2, 2), 4: (2, 2)}[count]
            rows, cols = layout

            for idx, f in enumerate(selected, start=1):
                ax = fig.add_subplot(rows, cols, idx)
                df = dfs[f]
                refresh = detected[f]
                create_subplot(ax, df, f, refresh)

            if title is not None:
                fig.suptitle(title, fontsize=24)
                fig.subplots_adjust(
                    left=0.02,
                    right=0.98,
                    top=0.96,   # room for title
                    bottom=0.02,
                    hspace=0.08,
                    wspace=0.08
                )
            else:
                fig.subplots_adjust(
                    left=0.02,
                    right=0.98,
                    top=0.98,   # slightly tighter without title
                    bottom=0.02,
                    hspace=0.08,
                    wspace=0.08
                )

            plt.savefig(output_path)
            if auto_open_png:
                try:
                    os.startfile(output_path)
                except:
                    pass
            print(f"\nSaved {output_path}")
            print("\nWhat next?")
            print("1. Run again")
            print("2. Exit")

            choice = input("> ").strip()
            if choice == "1":
                main()
            return


        # ==================================================================
        #  FPS OVERLAY MODE
        # ==================================================================
        if mode == "FPS_OVERLAY":
            plot_fps_overlay(fig, dfs, selected)

            if title is not None:
                fig.suptitle(title, fontsize=24)

            if title is not None:
                fig.subplots_adjust(
                    left=0.02,
                    right=0.98,
                    top=0.96,
                    bottom=0.02,
                    hspace=0.08,
                    wspace=0.08
                )
            else:
                fig.subplots_adjust(
                    left=0.02,
                    right=0.98,
                    top=0.98,
                    bottom=0.02,
                    hspace=0.08,
                    wspace=0.08
                )

            plt.savefig(output_path)
            if auto_open_png:
                try:
                    os.startfile(output_path)
                except:
                    pass
            print(f"\nSaved {output_path}")
            print("\nWhat next?")
            print("1. Run again")
            print("2. Exit")

            choice = input("> ").strip()
            if choice == "1":
                main()
            return


        print("\nDone. Press Enter to exit.")
        input()

    except Exception as e:
        print("\n--- ERROR ---")
        print(e)
        print("\nPress Enter to exit.")
        input()


# ======================================================================
#  ENTRY POINT
# ======================================================================

if __name__ == "__main__":
    main()
