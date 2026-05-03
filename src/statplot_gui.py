# gui/statplot_gui.py

import os
import sys
import datetime as dt
import json

from collections import deque
from datetime import datetime

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QCheckBox,
    QMessageBox,
    QDialog,
    QScrollArea,
    QMenu,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)

from engine import (
    load_config,
    save_config,
    list_csv_files,
    get_default_stats_path,
    format_default_title,
    generate_plot,
)

from ui_state import load_ui_state, save_ui_state

from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import QTimer

class WrappedTightDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.wrapText = True  # enable wrapping inside delegate

    def sizeHint(self, option, index):
        # Recompute size based on wrapped text
        super().initStyleOption(option, index)
        fm = option.fontMetrics
        text = option.text

        # Width available for wrapping
        width = option.rect.width() if option.rect.width() > 0 else 300

        # Compute wrapped bounding box
        rect = fm.boundingRect(0, 0, width, 0, Qt.TextWordWrap, text)

        # Add minimal padding
        return QSize(rect.width(), rect.height() + 4)

MAX_FILES = 4
MAX_THUMBNAILS = 10

# Fixed preview max size (does NOT affect fullscreen)
PREVIEW_MAX_WIDTH = 3840
PREVIEW_MAX_HEIGHT = 2160


# ============================================================
# FULLSCREEN IMAGE VIEWER
# ============================================================

class FullscreenImageViewer(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(None)   # <-- force top-level window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._image_path = image_path

        self._original_pixmap = QPixmap(self._image_path)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)

        # Ensure we really go fullscreen
        self.showFullScreen()

        # Determine screen size
        screen = None
        if self.windowHandle() is not None:
            screen = self.windowHandle().screen()
        if screen is None:
            screen = QApplication.primaryScreen()

        if screen is not None:
            screen_size = screen.availableGeometry().size()
            if self._original_pixmap and not self._original_pixmap.isNull():
                scaled = self._original_pixmap.scaled(
                    screen_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.label.setPixmap(scaled)
        else:
            # Fallback: just show original
            if self._original_pixmap and not self._original_pixmap.isNull():
                self.label.setPixmap(self._original_pixmap)

    def mousePressEvent(self, event):
        self.close()


# ============================================================
# SETTINGS DIALOG
# ============================================================

class SettingsDialog(QDialog):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.setWindowTitle("OXRT-StatPlot Settings")
        self.config = config

        paths = config["paths"] if config.has_section("paths") else {}
        defaults = config["defaults"] if config.has_section("defaults") else {}
        ui = config["ui"] if config.has_section("ui") else {}

        self.stats_dir_edit = QLineEdit(paths.get("stats_dir", "auto"))
        self.output_dir_edit = QLineEdit(paths.get("output_dir", "auto"))

        self.res_combo = QComboBox()
        self.res_combo.addItems(["4k", "1440p", "1080p"])
        self.res_combo.setCurrentText(defaults.get("resolution", "4k"))

        self.smooth_combo = QComboBox()
        self.smooth_combo.addItems(["none", "light", "medium", "heavy"])
        self.smooth_combo.setCurrentText(defaults.get("smoothing", "medium"))

        self.refresh_combo = QComboBox()
        self.refresh_combo.addItems(["auto", "72", "80", "90", "120", "144", "full"])
        self.refresh_combo.setCurrentText(defaults.get("refresh_rate", "auto"))

        self.plot_mode_combo = QComboBox()
        self.plot_mode_combo.addItems(["split", "overlay", "ft_split", "ft_overlay"])
        self.plot_mode_combo.setCurrentText(defaults.get("plot_mode", "split"))

        self.title_mode_combo = QComboBox()
        self.title_mode_combo.addItems(["default", "none", "manual"])
        self.title_mode_combo.setCurrentText(defaults.get("title_mode", "default"))

        self.show_ascii_chk = QCheckBox("Show ASCII art on startup")
        self.show_ascii_chk.setChecked(ui.get("show_ascii_art", "yes").lower() == "yes")

        self.auto_open_chk = QCheckBox("Auto-open PNG after saving")
        self.auto_open_chk.setChecked(ui.get("auto_open_png", "yes").lower() == "yes")

        self.verbose_chk = QCheckBox("Verbose debug logging (engine.log)")
        self.verbose_chk.setChecked(ui.get("verbose", "no").lower() == "yes")

        form = QFormLayout()
        form.addRow("Stats directory:", self.stats_dir_edit)
        form.addRow("Output directory:", self.output_dir_edit)
        form.addRow("Default resolution:", self.res_combo)
        form.addRow("Default smoothing:", self.smooth_combo)
        form.addRow("Default refresh rate:", self.refresh_combo)
        form.addRow("Default plot mode:", self.plot_mode_combo)
        form.addRow("Title mode:", self.title_mode_combo)
        form.addRow("", self.show_ascii_chk)
        form.addRow("", self.auto_open_chk)
        form.addRow("", self.verbose_chk)

        btn_ok = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btn_row)
        self.setLayout(layout)

    def apply_to_config(self):
        cfg = self.config
        if not cfg.has_section("paths"):
            cfg.add_section("paths")
        if not cfg.has_section("defaults"):
            cfg.add_section("defaults")
        if not cfg.has_section("ui"):
            cfg.add_section("ui")

        cfg.set("paths", "stats_dir", self.stats_dir_edit.text().strip() or "auto")
        cfg.set("paths", "output_dir", self.output_dir_edit.text().strip() or "auto")

        cfg.set("defaults", "resolution", self.res_combo.currentText())
        cfg.set("defaults", "smoothing", self.smooth_combo.currentText())
        cfg.set("defaults", "refresh_rate", self.refresh_combo.currentText())
        cfg.set("defaults", "plot_mode", self.plot_mode_combo.currentText())
        cfg.set("defaults", "title_mode", self.title_mode_combo.currentText())

        cfg.set("ui", "show_ascii_art", "yes" if self.show_ascii_chk.isChecked() else "no")
        cfg.set("ui", "auto_open_png", "yes" if self.auto_open_chk.isChecked() else "no")
        cfg.set("ui", "verbose", "yes" if self.verbose_chk.isChecked() else "no")


# ============================================================
# MAIN WINDOW
# ============================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OXRT-StatPlot 1.0.2 (GUI)")
        self.resize(1500, 900)

        # ---------------------------------------------------------
        # Load configs
        # ---------------------------------------------------------
        self.config = load_config()       # engine defaults (never overwritten)
        self.ui_state = load_ui_state()   # GUI-only persistence (safe to rewrite)

        # Runtime state
        self.recent_images = deque(maxlen=MAX_THUMBNAILS)
        self.metadata_map = {}            # image_path → metadata
        self.current_image_path = None

        # ---------------------------------------------------------
        # Build UI first (menus, widgets, layout)
        # ---------------------------------------------------------
        self._build_menu()
        self._build_ui()
        self._load_stats_dir_and_files()
        self._apply_style()

        # ---------------------------------------------------------
        # Load last title (GUI state)
        # ---------------------------------------------------------
        last_title = self.ui_state.get("ui", "last_title", fallback="").strip()
        if last_title:
            self.title_edit.setText(last_title)

        # ---------------------------------------------------------
        # Load persistent thumbnails (AFTER UI + config fully loaded)
        # ---------------------------------------------------------
        saved = self.ui_state.get("ui", "recent_images", fallback="")
        if saved:
            for p in saved.split("|"):
                if os.path.isfile(p):
                    self.recent_images.append(p)

                    # Reload metadata for this image if available
                    base = os.path.basename(p).lower()
                    key = f"meta_{base}"
                    meta_str = self.ui_state.get("ui", key, fallback="")
                    if meta_str:
                        try:
                            loaded = json.loads(meta_str)

                            if "timestamp" in loaded and loaded["timestamp"]:
                                loaded["timestamp"] = datetime.fromisoformat(loaded["timestamp"])

                            self.metadata_map[p] = loaded
                        except Exception:
                            pass



        # Build the thumbnail strip
        self._rebuild_thumbnails()

    # ---------------- MENU ----------------

    def _build_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        act_quit = QAction("Exit", self)
        act_quit.triggered.connect(self.close)
        file_menu.addAction(act_quit)

        settings_menu = menubar.addMenu("&Settings")
        act_prefs = QAction("Preferences…", self)
        act_prefs.triggered.connect(self.open_settings)
        settings_menu.addAction(act_prefs)

        help_menu = menubar.addMenu("&Help")
        act_about = QAction("About", self)
        act_about.triggered.connect(self.show_about)
        help_menu.addAction(act_about)

    # ---------------- UI LAYOUT ----------------

    def _build_ui(self):
        central = QWidget()
        main_layout = QHBoxLayout(central)

        # LEFT PANEL
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.stats_label = QLabel("Stats directory: (auto)")

        # Filter + table
        filter_row = QHBoxLayout()
        filter_label = QLabel("Filter:")
        self.filter_edit = QLineEdit()
        filter_row.addWidget(filter_label)
        filter_row.addWidget(self.filter_edit)

        self.files_table = QTableWidget()
        self.files_table.setColumnCount(3)
        self.files_table.setHorizontalHeaderLabels(["Filename", "Date", "Size"])
        self.files_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.files_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.files_table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.files_table.setSortingEnabled(True)
#        self.files_table.setWordWrap(True)
        self.files_table.setMinimumHeight(200)
        self.files_table.setItemDelegate(WrappedTightDelegate(self.files_table))
        self.files_table.verticalHeader().setDefaultSectionSize(22)
        self.files_table.verticalHeader().setMinimumSectionSize(22)


        self.files_table.itemSelectionChanged.connect(self._update_selection_style)
        self.filter_edit.textChanged.connect(self._filter_files)

        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Split – FPS + CPU/GPU", "FPS_SPLIT")
        self.mode_combo.addItem("Overlay – FPS only", "FPS_OVERLAY")
        self.mode_combo.addItem("Frametime Distribution (Split)", "FT_DIST_SPLIT")
        self.mode_combo.addItem("Frametime Distribution (Overlay)", "FT_DIST_OVERLAY")

        self.refresh_combo = QComboBox()
        self.refresh_combo.addItem("AUTO (recommended)", "AUTO")
        self.refresh_combo.addItem("72 Hz", 72)
        self.refresh_combo.addItem("80 Hz", 80)
        self.refresh_combo.addItem("90 Hz", 90)
        self.refresh_combo.addItem("120 Hz", 120)
        self.refresh_combo.addItem("144 Hz", 144)
        self.refresh_combo.addItem("Full range (50–150 Hz)", "FULL")

        self.res_combo = QComboBox()
        self.res_combo.addItem("4K (3840×2160)", (38.4, 21.6))
        self.res_combo.addItem("1440p (2560×1440)", (25.6, 14.4))
        self.res_combo.addItem("1080p (1920×1080)", (19.2, 10.8))

        self.smooth_combo = QComboBox()
        self.smooth_combo.addItem("None (0 samples)", 0)
        self.smooth_combo.addItem("Light (8 samples)", 8)
        self.smooth_combo.addItem("Medium (20 samples)", 20)
        self.smooth_combo.addItem("Heavy (40 samples)", 40)

        self.title_edit = QLineEdit()
        self.no_title_chk = QCheckBox("No title (override)")
        self.use_default_title_chk = QCheckBox("Use default title if empty")
        self.use_default_title_chk.setChecked(True)
        self.auto_open_gui_chk = QCheckBox("Automatically open plot image on generation")
        self.auto_open_gui_chk.setChecked(
            self.ui_state.get("ui", "auto_open_png", fallback="yes").lower() == "yes"
        )
        btn_generate = QPushButton("Generate Plot")
        btn_generate.clicked.connect(self.on_generate_clicked)

        left_form = QFormLayout()
        left_form.addRow("Plot mode:", self.mode_combo)
        left_form.addRow("Refresh rate:", self.refresh_combo)
        left_form.addRow("Resolution:", self.res_combo)
        left_form.addRow("Smoothing:", self.smooth_combo)
        left_form.addRow("Title:", self.title_edit)
        left_form.addRow("", self.no_title_chk)
        left_form.addRow("", self.use_default_title_chk)
        left_form.addRow("", self.auto_open_gui_chk)

        left_layout.addWidget(self.stats_label)
        left_layout.addLayout(filter_row)
        left_layout.addWidget(self.files_table)
        left_layout.addLayout(left_form)
        left_layout.addWidget(btn_generate)
        left_layout.addStretch()

        # give table more vertical stretch
        left_layout.setStretch(left_layout.indexOf(self.files_table), 2)

        # RIGHT PANEL
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.preview_label = QLabel("No image yet.")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(800, 450)
        self.preview_label.setStyleSheet("border: 1px solid #444;")
        self.preview_label.mousePressEvent = self._preview_clicked

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(160)
        thumb_container = QWidget()
        self.thumb_layout = QHBoxLayout(thumb_container)
        thumb_container.setMaximumHeight(150)
        scroll.setWidget(thumb_container)

        right_layout.addWidget(QLabel("Last generated plot:"))
        right_layout.addWidget(self.preview_label, stretch=1)
        right_layout.addWidget(QLabel("Recent plots:"))
        right_layout.addWidget(scroll, stretch=0)

        # SPLITTER
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([600, 900])
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.splitter)
        self.setCentralWidget(central)

    # ---------------- STYLE ----------------

    def _apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #101018;
                color: #f0f0f0;
            }
            QLabel {
                color: #f0f0f0;
            }
            QTableWidget {
                background-color: #181828;
                color: #f0f0f0;
                border: 1px solid #333;
                gridline-color: #333;
            }
            QHeaderView::section {
                background-color: #181828;
                color: #f0f0f0;
                border: 1px solid #333;
            }
            QLineEdit, QComboBox {
                background-color: #181828;
                color: #f0f0f0;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #2b2b3b;
                color: #f0f0f0;
                border: 1px solid #555;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #3b3b5b;
            }
            QCheckBox {
                color: #f0f0f0;
            }
            QMenuBar {
                background-color: #181828;
                color: #f0f0f0;
            }
            QMenu {
                background-color: #181828;
                color: #f0f0f0;
            }
        """)

    # ---------------- LOAD CSV FILES ----------------

    def _load_stats_dir_and_files(self):
        stats_dir = self.config.get("paths", "stats_dir", fallback="auto")
        if stats_dir.lower() == "auto":
            default_stats = get_default_stats_path()
            if default_stats and os.path.isdir(default_stats):
                self.resolved_stats = default_stats
            else:
                self.resolved_stats = None
        else:
            self.resolved_stats = stats_dir if os.path.isdir(stats_dir) else None

        if not self.resolved_stats:
            self.stats_label.setText("Stats directory: (not set)")
            self.files_table.setRowCount(0)
            return

        self.stats_label.setText(f"Stats directory: {self.resolved_stats}")
        files = list_csv_files(self.resolved_stats)
        self.files_table.setRowCount(len(files))

        for row, f in enumerate(files):
            full_path = os.path.join(self.resolved_stats, f)
            try:
                mtime = os.path.getmtime(full_path)
                size = os.path.getsize(full_path)
            except OSError:
                mtime = None
                size = 0

            name_item = QTableWidgetItem(f)
            name_item.setToolTip(f)
            date_str = ""
            if mtime is not None:
                date_str = datetime.fromtimestamp(mtime).strftime("%d/%m %H:%M")
            date_item = QTableWidgetItem(date_str)
            size_item = QTableWidgetItem(self._format_size(size))

            for item in (name_item, date_item, size_item):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            self.files_table.setItem(row, 0, name_item)
            self.files_table.setItem(row, 1, date_item)
            self.files_table.setItem(row, 2, size_item)

#        self.files_table.resizeRowsToContents()
        self.files_table.setColumnWidth(0, 350)
        self.files_table.setColumnWidth(1, 110)
        self.files_table.setColumnWidth(2, 90)

    def _format_size(self, size_bytes: int) -> str:
        if size_bytes <= 0:
            return "0 B"
        units = ["B", "KB", "MB", "GB", "TB"]
        idx = 0
        size = float(size_bytes)
        while size >= 1024 and idx < len(units) - 1:
            size /= 1024.0
            idx += 1
        if idx == 0:
            return f"{int(size)} {units[idx]}"
        return f"{size:.2f} {units[idx]}"

    # ---------------- FILTER ----------------

    def _filter_files(self, text: str):
        text = text.lower().strip()
        for row in range(self.files_table.rowCount()):
            name = self.files_table.item(row, 0).text().lower()
            hide = text not in name
            self.files_table.setRowHidden(row, hide)

    # ---------------- SETTINGS ----------------

    def open_settings(self):
        dlg = SettingsDialog(self, self.config)
        if dlg.exec() == QDialog.Accepted:
            dlg.apply_to_config()
            save_config(self.config)
            self._load_stats_dir_and_files()

    # ---------------- ABOUT ----------------

    def show_about(self):
        QMessageBox.information(
            self,
            "About OXRT-StatPlot",
            "OXRT-StatPlot 1.0.2\n\nAuthor: 75Vette / The Beast\nOXRT-StatPlot is a portable, zero-install Windows utility for analysing performance logs generated by the OpenXR Toolkit."
        )

    # ---------------- TITLE PERSISTENCE ----------------

    def _load_last_title(self):
        last_title = self.ui_state.get("ui", "last_title", fallback="").strip()
        if last_title:
            self.title_edit.setText(last_title)

    def _save_last_title(self, title: str):
        self.ui_state.set("ui", "last_title", title)
        save_ui_state(self.ui_state)



    # ---------------- GENERATE PLOT ----------------

    def on_generate_clicked(self):
        if not self.resolved_stats or not os.path.isdir(self.resolved_stats):
            QMessageBox.warning(self, "Stats directory", "Stats directory is not set or invalid.\nConfigure it in Settings.")
            return

        selected_rows = self.files_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No logs selected", "Select at least one CSV log (up to 4).")
            return
        if len(selected_rows) > MAX_FILES:
            QMessageBox.warning(self, "Too many logs", f"Select at most {MAX_FILES} logs.")
            return

        selected_files = [
            self.files_table.item(r.row(), 0).text()
            for r in selected_rows
        ]

        mode = self.mode_combo.currentData()
        refresh_choice = self.refresh_combo.currentData()
        resolution = self.res_combo.currentData()
        smoothing_window = self.smooth_combo.currentData()

        title = None
        if self.no_title_chk.isChecked():
            title = None
        else:
            raw = self.title_edit.text().strip()
            if raw:
                title = raw
                self._save_last_title(raw)
            elif self.use_default_title_chk.isChecked():
                title = format_default_title()
            else:
                title = None

        output_dir_cfg = self.config.get("paths", "output_dir", fallback="auto")
        auto_open_png = self.auto_open_gui_chk.isChecked()
        verbose = self.config.get("ui", "verbose", fallback="no").lower() == "yes"

        if not self.config.has_section("ui"):
            self.config.add_section("ui")

        self.ui_state.set(
            "ui",
            "auto_open_png",
            "yes" if self.auto_open_gui_chk.isChecked() else "no"
        )
        save_ui_state(self.ui_state)


        try:
            metadata = generate_plot(
                stats_dir=self.resolved_stats,
                output_dir=output_dir_cfg,
                selected_files=selected_files,
                mode=mode,
                refresh_choice=refresh_choice,
                resolution=resolution,
                smoothing_window=smoothing_window,
                title=title,
                auto_open_png=auto_open_png,
                verbose=verbose,
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")
            return

        out_path = metadata["output_path"]
        self.metadata_map[out_path] = metadata

        self._add_recent_image(out_path)
        self._set_preview_image(out_path)

    # ---------------- PREVIEW ----------------

    def _preview_clicked(self, event):
        if event.button() == Qt.LeftButton and self.current_image_path:
            pix = QPixmap(self.current_image_path)
            if pix.isNull():
                return
            viewer = FullscreenImageViewer(self.current_image_path)
            viewer.exec()

    def _set_preview_image(self, path, target_size=None):
        if not os.path.isfile(path):
            self.preview_label.setText("Image not found.")
            self.current_image_path = None
            return
        pix = QPixmap(path)
        if pix.isNull():
            self.preview_label.setText("Failed to load image.")
            self.current_image_path = None
            return

        self.current_image_path = path

        # First cap the pixmap to 4K max (for memory safety)
        pix = pix.scaled(
            QSize(PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # Then scale *again* to fit the preview widget
        if target_size is None:
            target_size = self.preview_label.size()

        scaled = pix.scaled(
            target_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.preview_label.setPixmap(scaled)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_image_path:
            # Defer until after layout has updated the label size
            QTimer.singleShot(0, lambda: self._set_preview_image(self.current_image_path))

    # ---------------- SELECTION VISUAL FEEDBACK ----------------

    def _update_selection_style(self):
        selected_rows = self.files_table.selectionModel().selectedRows()
        if len(selected_rows) > MAX_FILES:
            self.files_table.setStyleSheet("""
                QTableWidget {
                    background-color: #181828;
                    color: #f0f0f0;
                    border: 1px solid #333;
                    gridline-color: #333;
                }
                QHeaderView::section {
                    background-color: #181828;
                    color: #f0f0f0;
                    border: 1px solid #333;
                }
                QTableWidget::item:selected {
                    background-color: #802222;
                }
            """)
        else:
            self.files_table.setStyleSheet("""
                QTableWidget {
                    background-color: #181828;
                    color: #f0f0f0;
                    border: 1px solid #333;
                    gridline-color: #333;
                }
                QHeaderView::section {
                    background-color: #181828;
                    color: #f0f0f0;
                    border: 1px solid #333;
                }
                QTableWidget::item:selected {
                    background-color: #3b3b5b;
                }
            """)

    # ---------------- THUMBNAILS ----------------

    def _add_recent_image(self, path):
        # If the newest is the same path, ignore duplicate call
        if self.recent_images and self.recent_images[0] == path:
            return

        # Remove any older occurrences of this path
        while path in self.recent_images:
            self.recent_images.remove(path)

        self.recent_images.appendleft(path)
        self._rebuild_thumbnails()

        # Persist recent thumbnails immediately (crash‑safe)
        self.ui_state.set("ui", "recent_images", "|".join(self.recent_images))

        # Persist metadata for this image
        meta = self.metadata_map.get(path, {})
        base = os.path.basename(path).lower()
        key = f"meta_{base}"
        safe_meta = dict(meta)

        if "timestamp" in safe_meta and safe_meta["timestamp"] is not None:
            safe_meta["timestamp"] = safe_meta["timestamp"].isoformat()

        self.ui_state.set("ui", key, json.dumps(safe_meta))

        save_ui_state(self.ui_state)


    def _rebuild_thumbnails(self):
        while self.thumb_layout.count():
            item = self.thumb_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        for path in self.recent_images:
            container = QWidget()
            v = QVBoxLayout(container)
            v.setContentsMargins(0, 0, 0, 0)
            v.setSpacing(2)

            thumb = QLabel()
            thumb.setFixedSize(QSize(200, 120))
            thumb.setStyleSheet("border: 1px solid #555;")
            pix = QPixmap(path)
            if not pix.isNull():
                scaled = pix.scaled(
                    thumb.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                thumb.setPixmap(scaled)

            thumb.mousePressEvent = self._make_thumb_mouse_handler(path)

            caption = QLabel(self._build_thumbnail_caption(path))
            caption.setAlignment(Qt.AlignCenter)
            caption.setStyleSheet("font-size: 10px; color: #cccccc;")

            v.addWidget(thumb)
            v.addWidget(caption)

            self.thumb_layout.addWidget(container)

        self.thumb_layout.addStretch()

    def _build_thumbnail_caption(self, image_path):
        meta = self.metadata_map.get(image_path)
        if not meta:
            return ""

        ts = meta.get("timestamp")
        if ts is None:
            return ""

        ts_str = ts.strftime("%d/%m %H:%M")

        refresh_map = meta.get("refresh_rates", {})
        unique_rates = set(refresh_map.values())

        if not unique_rates:
            hz_str = ""
        elif len(unique_rates) == 1:
            val = list(unique_rates)[0]
            if isinstance(val, str) and val.upper() == "FULL":
                hz_str = "Full"
            else:
                hz_str = f"{val}Hz"
        else:
            hz_str = "Multiple Hz"

        if hz_str:
            return f"{ts_str} {hz_str}"
        return ts_str

    def _make_thumb_mouse_handler(self, path):
        def handler(event):
            if event.button() == Qt.LeftButton:
                self._set_preview_image(path)
            elif event.button() == Qt.RightButton:
                self._show_thumb_context_menu(path, event.globalPosition().toPoint())
        return handler

    def _show_thumb_context_menu(self, image_path, global_pos):
        menu = QMenu(self)

        act_open_png = QAction("Open PNG in Explorer", self)
        act_open_png.triggered.connect(
            lambda: self._open_file_in_explorer(image_path)
        )
        menu.addAction(act_open_png)

        meta = self.metadata_map.get(image_path)
        if meta:
            selected_files = meta.get("selected_files", [])
            if selected_files and self.resolved_stats:
                act_open_csv = QAction("Open CSV in Explorer", self)
                act_open_csv.triggered.connect(
                    lambda: self._open_file_in_explorer(
                        os.path.join(self.resolved_stats, selected_files[0])
                    )
                )
                menu.addAction(act_open_csv)

        menu.exec(global_pos)

    def _open_file_in_explorer(self, path):
        if os.path.exists(path):
            try:
                os.system(f'explorer /select,"{path}"')
            except Exception:
                folder = os.path.dirname(path)
                if os.path.isdir(folder):
                    try:
                        os.startfile(folder)
                    except Exception:
                        pass


# ============================================================
# ENTRY POINT
# ============================================================

import sys
import os
import subprocess


if __name__ == "__main__":
    # GUI MODE ONLY (CLI Depreciated in 1.0.0)
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
