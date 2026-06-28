import os
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.settings import load_settings
from app.ui.tools.base_tool_widget import TOOL_CONTENT_HORIZONTAL_MARGIN
from app.utils.i18n import tr

_SIDEBAR_WIDTH = 268
_THEME_BAR_H_PAD = 12
_CONTROL_HEIGHT = 36
_FONT_PX = 13
_LEFT_PREFIX_WIDTH = (
    _SIDEBAR_WIDTH + TOOL_CONTENT_HORIZONTAL_MARGIN - _THEME_BAR_H_PAD
)
_BAR_HEIGHT = _CONTROL_HEIGHT + 16 + 6


class OutputBar(QWidget):
    run_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("outputBar")
        self.setContentsMargins(0, 8, 0, 8)
        self._progress_total = 0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(6)

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedHeight(6)
        self._progress_bar.setVisible(False)
        outer.addWidget(self._progress_bar)

        layout = QHBoxLayout()
        layout.setContentsMargins(
            0,
            0,
            TOOL_CONTENT_HORIZONTAL_MARGIN,
            6,
        )
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        left_zone = QWidget()
        left_zone.setFixedWidth(_LEFT_PREFIX_WIDTH)
        left_layout = QHBoxLayout(left_zone)
        left_layout.setContentsMargins(TOOL_CONTENT_HORIZONTAL_MARGIN, 0, 8, 0)
        left_layout.setSpacing(8)

        self._output_label = QLabel()
        self._output_label.setObjectName("outputLabel")
        self._output_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        left_layout.addWidget(
            self._output_label, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(left_zone)

        right_zone = QWidget()
        right_zone.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        right_layout = QHBoxLayout(right_zone)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._path_edit = QLineEdit()
        self._path_edit.setObjectName("outputInput")
        self._path_edit.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        self._path_edit.setFixedHeight(_CONTROL_HEIGHT)
        self._path_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        desktop = Path(os.path.expanduser("~")) / "Desktop"
        self._path_edit.setText(str(desktop))
        self._output_dir = desktop
        right_layout.addWidget(self._path_edit, 1)

        self._browse_btn = QPushButton()
        self._browse_btn.setObjectName("outputBtn")
        self._browse_btn.setFixedHeight(_CONTROL_HEIGHT)
        self._browse_btn.clicked.connect(self._browse_output_dir)
        right_layout.addWidget(
            self._browse_btn, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        self._run_btn = QPushButton()
        self._run_btn.setObjectName("convertBtn")
        self._run_btn.setMinimumWidth(100)
        self._run_btn.clicked.connect(self.run_requested.emit)
        right_layout.addWidget(
            self._run_btn, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(right_zone, 1)

        outer.addLayout(layout)

        self._apply_control_fonts()
        self.setFixedHeight(_BAR_HEIGHT)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.set_running(False)
        self.retranslate()
        QTimer.singleShot(0, self._sync_run_button_height)

    def _apply_control_fonts(self) -> None:
        font = QFont()
        font.setPixelSize(_FONT_PX)
        for widget in (
            self._output_label,
            self._path_edit,
            self._browse_btn,
            self._run_btn,
        ):
            widget.setFont(font)
        self._path_edit.setFixedHeight(_CONTROL_HEIGHT)
        self._browse_btn.setFixedHeight(_CONTROL_HEIGHT)
        self._sync_run_button_height()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._sync_run_button_height()

    def _sync_run_button_height(self) -> None:
        browse_height = self._browse_btn.height()
        if browse_height <= 0:
            browse_height = self._browse_btn.sizeHint().height()
        if browse_height <= 0:
            browse_height = _CONTROL_HEIGHT
        self._run_btn.setFixedHeight(browse_height)

    @property
    def output_dir(self) -> Path:
        text = self._path_edit.text().strip()
        if text:
            return Path(text)
        return self._output_dir

    @property
    def overwrite(self) -> bool:
        return load_settings().overwrite

    @property
    def suffix(self) -> str:
        return load_settings().suffix

    def set_running(self, state: bool) -> None:
        self._run_btn.setEnabled(not state)
        self._path_edit.setEnabled(not state)
        self._browse_btn.setEnabled(not state)

    def start_progress(self, total: int) -> None:
        self._progress_total = max(1, total)
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setVisible(True)

    def update_progress(self, current: int, total: int | None = None) -> None:
        if total is not None:
            self._progress_total = max(1, total)
        value = int(current * 100 / self._progress_total)
        self._progress_bar.setValue(max(0, min(100, value)))

    def finish_progress(self) -> None:
        self._progress_bar.setValue(100)
        QTimer.singleShot(500, self._hide_progress)

    def reset_progress(self) -> None:
        self._hide_progress()

    def _hide_progress(self) -> None:
        self._progress_bar.setVisible(False)
        self._progress_bar.setValue(0)

    def retranslate(self) -> None:
        self._apply_control_fonts()
        self._output_label.setText(tr("output_folder"))
        self._path_edit.setPlaceholderText(tr("output_path_placeholder"))
        self._browse_btn.setText(tr("browse"))
        self._run_btn.setText(tr("run"))
        self._sync_run_button_height()

    def _browse_output_dir(self) -> None:
        start = self._path_edit.text() or str(Path.home())
        folder = QFileDialog.getExistingDirectory(self, tr("output_folder"), start)
        if folder:
            self._path_edit.setText(folder)
            self._output_dir = Path(folder)
