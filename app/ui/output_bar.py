from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from app.settings import load_settings
from app.utils.i18n import tr


class OutputBar(QWidget):
    run_requested = pyqtSignal()
    cancel_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        settings = load_settings()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._output_label = QLabel()
        layout.addWidget(self._output_label)

        self._path_edit = QLineEdit()
        self._path_edit.setText(settings.last_output_dir)
        layout.addWidget(self._path_edit, 1)

        self._browse_btn = QPushButton()
        self._browse_btn.clicked.connect(self._browse_output_dir)
        layout.addWidget(self._browse_btn)

        self._overwrite_cb = QCheckBox()
        self._overwrite_cb.setChecked(settings.overwrite)
        layout.addWidget(self._overwrite_cb)

        self._suffix_edit = QLineEdit()
        self._suffix_edit.setText(settings.suffix)
        self._suffix_edit.setMaximumWidth(120)
        layout.addWidget(self._suffix_edit)

        self._run_btn = QPushButton()
        self._run_btn.setObjectName("primary")
        self._run_btn.clicked.connect(self.run_requested.emit)
        layout.addWidget(self._run_btn)

        self._cancel_btn = QPushButton()
        self._cancel_btn.clicked.connect(self.cancel_requested.emit)
        layout.addWidget(self._cancel_btn)

        self.set_running(False)
        self.retranslate()

    @property
    def output_dir(self) -> Path:
        return Path(self._path_edit.text())

    @property
    def overwrite(self) -> bool:
        return self._overwrite_cb.isChecked()

    @property
    def suffix(self) -> str:
        return self._suffix_edit.text()

    def set_running(self, state: bool) -> None:
        self._run_btn.setEnabled(not state)
        self._cancel_btn.setEnabled(state)

    def retranslate(self) -> None:
        self._output_label.setText(tr("output_folder"))
        self._browse_btn.setText(tr("browse"))
        self._overwrite_cb.setText(tr("overwrite"))
        self._suffix_edit.setPlaceholderText(tr("suffix"))
        self._run_btn.setText(tr("run"))
        self._cancel_btn.setText(tr("cancel"))

    def _browse_output_dir(self) -> None:
        start = self._path_edit.text() or str(Path.home())
        folder = QFileDialog.getExistingDirectory(self, tr("output_folder"), start)
        if folder:
            self._path_edit.setText(folder)
