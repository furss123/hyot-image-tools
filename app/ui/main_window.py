from __future__ import annotations

import importlib

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.constants import TOOL_IDS
from app.settings import Settings, save_settings
from app.ui.log_panel import LogPanel
from app.ui.output_bar import OutputBar
from app.ui.sidebar import Sidebar
from app.ui.theme import get_stylesheet
from app.utils.i18n import load, tr


class MainWindow(QMainWindow):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        load(settings.language)
        self._tool_widgets: dict[str, QWidget] = {}
        self._tool_indices: dict[str, int] = {}
        self._build_ui()
        self.setWindowTitle(tr("app_title"))
        self.setMinimumSize(1100, 700)
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(get_stylesheet(settings.theme))
        self.retranslate()
        last_tool = (
            settings.last_tool
            if settings.last_tool in TOOL_IDS
            else TOOL_IDS[0]
        )
        self._on_tool_selected(last_tool)
        self.sidebar.set_active(last_tool)

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        self.sidebar.setFixedWidth(200)
        self.sidebar.tool_selected.connect(self._on_tool_selected)
        layout.addWidget(self.sidebar)

        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(0)

        self._stack = QStackedWidget()
        right.addWidget(self._stack, 1)

        for tool_id in TOOL_IDS:
            widget = self._create_tool_widget(tool_id)
            self._tool_widgets[tool_id] = widget
            self._tool_indices[tool_id] = self._stack.addWidget(widget)

        self.output_bar = OutputBar()
        right.addWidget(self.output_bar)

        self.log_panel = LogPanel()
        right.addWidget(self.log_panel)

        layout.addLayout(right, 1)

    def _create_tool_widget(self, tool_id: str) -> QWidget:
        module = importlib.import_module(f"app.ui.tools.{tool_id}")
        class_name = "".join(part.capitalize() for part in tool_id.split("_")) + "ToolWidget"
        widget_cls = getattr(module, class_name, None) or getattr(module, "ToolWidget", None)
        if widget_cls is not None:
            return widget_cls()
        return QWidget()

    def _on_tool_selected(self, tool_id: str) -> None:
        if tool_id not in self._tool_indices:
            return
        self._stack.setCurrentIndex(self._tool_indices[tool_id])
        self.settings.last_tool = tool_id
        save_settings(self.settings)

    def switch_theme(self, theme: str) -> None:
        self.settings.theme = theme
        save_settings(self.settings)
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(get_stylesheet(theme))

    def switch_language(self, lang: str) -> None:
        self.settings.language = lang
        save_settings(self.settings)
        load(lang)
        self.retranslate()

    def retranslate(self) -> None:
        self.setWindowTitle(tr("app_title"))
        self.sidebar.retranslate()
        self.output_bar.retranslate()
        self.log_panel.retranslate()
        for widget in self._tool_widgets.values():
            if hasattr(widget, "retranslate"):
                widget.retranslate()
