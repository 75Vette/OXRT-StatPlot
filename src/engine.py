# core/engine.py

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
#  COLOR PALETTE
# ======================================================================

NEON_FPS_COLORS = ["#f5f749", "#4df2ff", "#7CFF6B", "#ff4df2", "#ffb84d", "#c44dff"]

COLOR_FPS = "#f5f749"
COLOR_CPU_APP = "#ff4df2"
COLOR_CPU_RENDER = "#c44dff"
COLOR_GPU = "#7CFF6B"
COLOR_GUIDE = "#AAAAAA"

KNOWN_REFRESH_RATES = [72, 80, 90, 120, 144]

FT_OVERLAY_PAIRS = [
    ("#f5f749", "#ffb84d"),   # yellow + orange
    ("#4df2ff", "#0099cc"),   # cyan + deep blue
    ("#7CFF6B", "#2ea043"),   # neon green + dark green
    ("#ff4df2", "#c44dff"),   # neon pink + magenta
]

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


[ui]
# Console size (CLI only; currently informational)
console_width = {console_width}
console_height = {console_height}

# Show ASCII art banner on startup (yes/no)
show_ascii_art = {show_ascii_art}

# Automatically open PNG after saving (yes/no)
auto_open_png = {auto_open_png}

# Verbose mode prints extra debug info (yes/no)
verbose = {verbose}

# Recent plot thumbnails (GUI; pipe-separated PNG paths)
recent_images = {recent_images}

# Last used manual title (GUI)
last_title = {last_title}
"""


# ======================================================================
#  DEBUG LOGGING
# ======================================================================

from app_paths import (
    CONFIG_PATH,
    LOG_PATH,
    RESULTS_DIR,
)

def get_config_path():
    return str(CONFIG_PATH)

def get_log_path():
    return str(LOG_PATH)

def log_debug(message, enabled=False):
    if not enabled:
        return
    try:
        log_path = get_log_path()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {message}\n")
    except Exception:
        # Debug logging must never break the engine
        pass

# ======================================================================
#  CONFIG HANDLING
# ======================================================================

def load_config():
    """
    Load config.ini if present; if missing, create one with factory defaults.
    Returns a ConfigParser instance.
    """
    config_path = get_config_path()

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
            "auto_open_png": "yes",
            "verbose": "no",
        },

    }

    config = configparser.ConfigParser()
    if os.path.isfile(config_path):
        config.read(config_path)
    else:
        write_config_from_values(defaults)
        config.read(config_path)

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
    recent_images = ui.get("recent_images", "")
    last_title = ui.get("last_title", "")

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
        recent_images=recent_images,
        last_title=last_title,
    )

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(text)

def save_config(config):
    """
    Save config.ini while preserving ALL existing keys,
    including GUI‑added ones like recent_images and last_title.
    """
    config_path = get_config_path()

    # Load existing config if present
    merged = configparser.ConfigParser()
    if os.path.isfile(config_path):
        merged.read(config_path)

    # Ensure all sections exist
    for section in config.sections():
        if not merged.has_section(section):
            merged.add_section(section)

    # Copy all keys from the provided config into merged config
    for section in config.sections():
        for key, val in config.items(section):
            merged.set(section, key, val)

    # Write merged config back to disk
    with open(config_path, "w", encoding="utf-8") as f:
        merged.write(f)


# ======================================================================
#  PATH HELPERS
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

def list_csv_files(directory):
    files = [
        f for f in os.listdir(directory)
        if f.lower().endswith(".csv")
    ]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    return files

# ======================================================================
#  TITLE HELPERS
# ======================================================================

def format_default_title():
    try:
        loc = locale.getlocale()[0] or ""
    except Exception:
        loc = ""
    now = datetime.now()
    if loc.startswith("en_US"):
        date_str = now.strftime("%m/%d/%y")
    else:
        date_str = now.strftime("%d/%m/%y")
    time_str = now.strftime("%H:%M")
    return f"OpenXR Toolkit Stat Plot – {time_str} {date_str}"

# ======================================================================
#  DATA LOADING + PROCESSING
# ======================================================================

def load_and_process(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df["time"] = pd.to_datetime(df["time"])
    df["elapsed_min"] = (df["time"] - df["time"].min()).dt.total_seconds() / 60

    df["appCPU_ms"] = df["appCPU (us)"] / 1000.0
    df["renderCPU_ms"] = df["renderCPU (us)"] / 1000.0
    df["appGPU_ms"] = df["appGPU (us)"] / 1000.0

    return df

def apply_smoothing(df, window):
    if window <= 0:
        return df
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
    return df

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

def fps_range_for_refresh(refresh):
    if refresh == "FULL":
        return (50, 150)
    lower = max(42, refresh - 30)
    upper = refresh + 10
    return (lower, upper)

# ======================================================================
#  GUIDE LINES
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
#  FPS SPLIT SUBPLOT
# ======================================================================

def create_subplot(ax, df, filename, refresh):
    fps_range = fps_range_for_refresh(refresh)
    handles = []

    if "FPS_smooth" in df.columns:
        ax.plot(df["elapsed_min"], df["FPS"], color=COLOR_FPS, alpha=0.25, linewidth=1.0)
        fps_line, = ax.plot(
            df["elapsed_min"], df["FPS_smooth"],
            color=COLOR_FPS, alpha=1.0, linewidth=2.0,
            label="FPS (smoothed)"
        )
    else:
        fps_line, = ax.plot(
            df["elapsed_min"], df["FPS"],
            color=COLOR_FPS, linewidth=1.5, label="FPS"
        )

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

        cpu_app_line, = ax_r.plot(
            df["elapsed_min"], df["appCPU_ms_smooth"],
            color=COLOR_CPU_APP, alpha=1.0, linewidth=2.0,
            label="CPU App (smoothed)"
        )
        cpu_render_line, = ax_r.plot(
            df["elapsed_min"], df["renderCPU_ms_smooth"],
            color=COLOR_CPU_RENDER, alpha=1.0, linewidth=2.0,
            label="CPU Render (smoothed)"
        )
        gpu_line, = ax_r.plot(
            df["elapsed_min"], df["appGPU_ms_smooth"],
            color=COLOR_GPU, alpha=1.0, linewidth=2.0,
            label="GPU (smoothed)"
        )
    else:
        cpu_app_line, = ax_r.plot(
            df["elapsed_min"], df["appCPU_ms"],
            color=COLOR_CPU_APP, linewidth=1.5, label="CPU App"
        )
        cpu_render_line, = ax_r.plot(
            df["elapsed_min"], df["renderCPU_ms"],
            color=COLOR_CPU_RENDER, linewidth=1.5, label="CPU Render"
        )
        gpu_line, = ax_r.plot(
            df["elapsed_min"], df["appGPU_ms"],
            color=COLOR_GPU, linewidth=1.5, label="GPU"
        )

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
            line, = ax.plot(
                df["elapsed_min"], df["FPS_smooth"],
                color=color, alpha=1.0, linewidth=2.0, label=f
            )
        else:
            line, = ax.plot(
                df["elapsed_min"], df["FPS"],
                color=color, linewidth=1.5, label=f
            )

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
#  FRAMETIME DISTRIBUTION
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
#  ENGINE ORCHESTRATOR
# ======================================================================

def generate_plot(
    stats_dir,
    output_dir,
    selected_files,
    mode,
    refresh_choice,
    resolution,
    smoothing_window,
    title,
    auto_open_png=True,
    verbose=False,
):
    """
    Core engine entry point.

    All arguments are already chosen by CLI/GUI.
    No user input, no printing.

    Returns a rich metadata dict.
    """

    debug = verbose
    log_debug(f"generate_plot called with mode={mode}, files={selected_files}", debug)

    # Resolve stats_dir and output_dir (no chdir here; use absolute paths)
    if stats_dir.lower() == "auto":
        default_stats = get_default_stats_path()
        if default_stats and os.path.isdir(default_stats):
            resolved_stats_dir = default_stats
        else:
            raise FileNotFoundError("Auto stats_dir could not be resolved.")
    else:
        if not os.path.isdir(stats_dir):
            raise FileNotFoundError(f"Configured stats_dir is invalid: {stats_dir}")
        resolved_stats_dir = stats_dir

    if output_dir.lower() == "auto":
        resolved_output_dir = str(RESULTS_DIR)
    else:
        resolved_output_dir = output_dir

    os.makedirs(resolved_output_dir, exist_ok=True)

    log_debug(f"Resolved stats_dir={resolved_stats_dir}", debug)
    log_debug(f"Resolved output_dir={resolved_output_dir}", debug)

    # Load dataframes
    dfs = {}
    for f in selected_files:
        full_path = os.path.join(resolved_stats_dir, f)
        df = load_and_process(full_path)
        if smoothing_window > 0:
            df = apply_smoothing(df, smoothing_window)
        dfs[f] = df

    # Detect refresh per file if AUTO
    detected = {}
    if refresh_choice == "AUTO":
        for f, df in dfs.items():
            hz = auto_detect_refresh_rate(df)
            detected[f] = hz if hz else "FULL"
    else:
        for f in selected_files:
            detected[f] = refresh_choice

    log_debug(f"Detected refresh map: {detected}", debug)

    # Build output filename
    now = datetime.now()
    date_str = now.strftime("%d-%b-%y")
    time_str = now.strftime("%H%M%S")  # include seconds for uniqueness

    safe_title = title or "No Title"
    safe_title = "".join(
        c for c in safe_title if c.isalnum() or c in (" ", "-")
    )

    output_name = f"OXRT StatPlot {date_str} - {time_str} - {safe_title}.png"
    output_path = os.path.join(resolved_output_dir, output_name)

    # Create figure
    fig = plt.figure(figsize=resolution, dpi=100)

    # Plot according to mode
    if mode == "FT_DIST_SPLIT":
        plot_ft_dist_split(fig, dfs, selected_files)
        if title is not None:
            fig.suptitle(title, fontsize=24)
        fig.savefig(output_path)

    elif mode == "FT_DIST_OVERLAY":
        plot_ft_dist_overlay(fig, dfs, selected_files)
        if title is not None:
            fig.suptitle(title, fontsize=24)
        fig.savefig(output_path)

    elif mode == "FPS_SPLIT":
        count = len(selected_files)
        layout = {1: (1, 1), 2: (2, 1), 3: (2, 2), 4: (2, 2)}[count]
        rows, cols = layout

        for idx, f in enumerate(selected_files, start=1):
            ax = fig.add_subplot(rows, cols, idx)
            df = dfs[f]
            refresh = detected[f]
            create_subplot(ax, df, f, refresh)

        if title is not None:
            fig.suptitle(title, fontsize=24)
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

        fig.savefig(output_path)

    elif mode == "FPS_OVERLAY":
        plot_fps_overlay(fig, dfs, selected_files)

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

        fig.savefig(output_path)

    else:
        plt.close(fig)
        raise ValueError(f"Unknown plot mode: {mode}")

    plt.close(fig)

    if auto_open_png:
        try:
            os.startfile(output_path)
        except Exception:
            pass

    log_debug(f"Saved plot to {output_path}", debug)

    # Rich metadata return
    metadata = {
        "output_path": output_path,
        "selected_files": list(selected_files),
        "plot_mode": mode,
        "refresh_rates": dict(detected),
        "smoothing_window": smoothing_window,
        "resolution": resolution,
        "title": title,
        "stats_dir": resolved_stats_dir,
        "output_dir": resolved_output_dir,
        "timestamp": now,
    }

    return metadata
