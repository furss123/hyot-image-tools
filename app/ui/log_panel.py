from datetime import datetime

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.utils.i18n import tr


class LogPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._expanded = True

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._toggle_btn = QPushButton()
        self._toggle_btn.setCheckable(True)
        self._toggle_btn.setChecked(True)
        self._toggle_btn.clicked.connect(self._on_toggle)
        layout.addWidget(self._toggle_btn)

        self._content = QWidget()
        content_layout = QVBoxLayout(self._content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(6)

        toolbar = QHBoxLayout()
        toolbar.addStretch(1)
        self._clear_btn = QPushButton()
        self._clear_btn.clicked.connect(self.clear)
        toolbar.addWidget(self._clear_btn)
        content_layout.addLayout(toolbar)

        self._log = QPlainTextEdit()
        self._log.setReadOnly(True)
        self._log.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        font = QFont("Consolas")
        font.setStyleHint(QFont.StyleHint.Monospace)
        self._log.setFont(font)
        content_layout.addWidget(self._log, 1)

        layout.addWidget(self._content, 1)
        self.retranslate()

    def append(self, msg: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._log.appendPlainText(f"[{timestamp}] {msg}")

    def clear(self) -> None:
        self._log.clear()

    def retranslate(self) -> None:
        self._update_toggle_text()
        self._clear_btn.setText(tr("clear_log"))

    def _on_toggle(self) -> None:
        self._expanded = self._toggle_btn.isChecked()
        self._content.setVisible(self._expanded)
        self._update_toggle_text()

    def _update_toggle_text(self) -> None:
        arrow = "▼" if self._expanded else "▶"
        self._toggle_btn.setText(f"{arrow} {tr('log_panel')}")
