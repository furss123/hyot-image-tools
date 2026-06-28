from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QWidget,
)

from app.utils.i18n import tr


class ProgressPanel(QWidget):
    cancel_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("progressPanel")
        self.setFixedHeight(36)
        self._current = 0
        self._total = 0
        self.hide()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(8)

        self._status_label = QLabel()
        self._status_label.setObjectName("progressLabel")
        layout.addWidget(self._status_label)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(4)
        layout.addWidget(self._bar, 1)

        self._cancel_btn = QPushButton()
        self._cancel_btn.setObjectName("cancelLink")
        self._cancel_btn.setFlat(True)
        self._cancel_btn.clicked.connect(self.cancel_requested.emit)
        layout.addWidget(self._cancel_btn)

        self.reset()

    def start(self, total: int) -> None:
        self._total = max(0, total)
        self._current = 0
        self._bar.setValue(0)
        self._update_label()
        self.show()

    def update_overall(self, current: int, total: int | None = None) -> None:
        if total is not None:
            self._total = max(0, total)
        self._current = current
        if self._total > 0:
            value = int(self._current * 100 / self._total)
            self._bar.setValue(max(0, min(100, value)))
        self._update_label()

    def finish(self) -> None:
        QTimer.singleShot(1500, self._hide_and_reset)

    def reset(self) -> None:
        self._current = 0
        self._total = 0
        self._bar.setValue(0)
        self._status_label.clear()

    def retranslate(self) -> None:
        self._cancel_btn.setText(tr("cancel"))
        self._update_label()

    def _update_label(self) -> None:
        if self._total > 0:
            self._status_label.setText(
                tr("progress_status")
                .replace("{current}", str(self._current))
                .replace("{total}", str(self._total))
            )

    def _hide_and_reset(self) -> None:
        self.hide()
        self.reset()
