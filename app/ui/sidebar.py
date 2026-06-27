from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.constants import ASSETS_DIR, TOOL_IDS
from app.ui.theme import DARK, LIGHT
from app.utils.i18n import tr

if TYPE_CHECKING:
    from app.ui.main_window import MainWindow


class Sidebar(QWidget):
    tool_selected = pyqtSignal(str)

    def __init__(self, main_window: MainWindow) -> None:
        super().__init__()
        self._main_window = main_window
        self._theme = main_window.settings.theme
        self._language = main_window.settings.language
        self._tool_rows: dict[str, int] = {}

        self.setFixedWidth(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(12)

        self._app_label = QLabel()
        layout.addWidget(self._app_label)

        self._tool_list = QListWidget()
        self._tool_list.setFrameShape(QListWidget.Shape.NoFrame)
        for row, tool_id in enumerate(TOOL_IDS):
            item = QListWidgetItem(tr(tool_id))
            icon_path = ASSETS_DIR / "icons" / f"{tool_id}.svg"
            if icon_path.is_file():
                item.setIcon(QIcon(str(icon_path)))
            self._tool_list.addItem(item)
            self._tool_rows[tool_id] = row
        self._tool_list.currentRowChanged.connect(self._on_tool_row_changed)
        layout.addWidget(self._tool_list, 1)

        self._theme_btn = QPushButton()
        self._theme_btn.clicked.connect(self._on_theme_toggle)
        layout.addWidget(self._theme_btn)

        self._lang_btn = QPushButton()
        self._lang_btn.clicked.connect(self._on_language_toggle)
        layout.addWidget(self._lang_btn)

        self._apply_chrome()
        self.retranslate()

    def set_active(self, tool_id: str) -> None:
        row = self._tool_rows.get(tool_id)
        if row is None:
            return
        self._tool_list.blockSignals(True)
        self._tool_list.setCurrentRow(row)
        self._tool_list.blockSignals(False)

    def retranslate(self) -> None:
        self._theme = self._main_window.settings.theme
        self._language = self._main_window.settings.language
        self._app_label.setText(tr("app_title"))
        for row, tool_id in enumerate(TOOL_IDS):
            item = self._tool_list.item(row)
            if item is not None:
                item.setText(tr(tool_id))
        self._theme_btn.setText(
            "☀ Light" if self._theme == "dark" else "🌙 Dark"
        )
        self._lang_btn.setText(
            "English" if self._language == "ko" else "한국어"
        )

    def _apply_chrome(self) -> None:
        tokens = LIGHT if self._theme == "light" else DARK
        self.setStyleSheet(f"background-color: {tokens['bg_surface']};")
        font = QFont(self._app_label.font())
        font.setBold(True)
        self._app_label.setFont(font)
        self._app_label.setStyleSheet(f"color: {tokens['accent']};")

    def _on_tool_row_changed(self, row: int) -> None:
        if row < 0 or row >= len(TOOL_IDS):
            return
        self.tool_selected.emit(TOOL_IDS[row])

    def _on_theme_toggle(self) -> None:
        new_theme = "light" if self._theme == "dark" else "dark"
        self._main_window.switch_theme(new_theme)
        self._theme = new_theme
        self._apply_chrome()
        self.retranslate()

    def _on_language_toggle(self) -> None:
        new_lang = "en" if self._language == "ko" else "ko"
        self._main_window.switch_language(new_lang)
