from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
)

from app.models.tool_options import BgRemoveOptions
from app.ui.tools.base_tool_widget import BaseToolWidget
from app.utils.i18n import tr


class BgRemoveToolWidget(BaseToolWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._model_combo = QComboBox()
        self._model_combo.addItem("", "u2net")
        self._model_combo.addItem("", "u2net_human_seg")
        self._model_label = QLabel()
        form.addRow(self._model_label, self._model_combo)

        self._feather_spin = QSpinBox()
        self._feather_spin.setRange(0, 20)
        self._feather_spin.setValue(0)
        self._feather_spin.setSuffix(" px")
        self._feather_label = QLabel()
        form.addRow(self._feather_label, self._feather_spin)

        layout.addLayout(form)

        self._info_label = QLabel()
        self._info_label.setWordWrap(True)
        layout.addWidget(self._info_label)

        self._download_label = QLabel()
        self._download_label.setWordWrap(True)
        layout.addWidget(self._download_label)

        layout.addStretch(1)
        self.retranslate()

    def get_options(self) -> BgRemoveOptions:
        return BgRemoveOptions(
            model=self._model_combo.currentData(),
            feather=self._feather_spin.value(),
        )

    def retranslate(self) -> None:
        self._model_label.setText(tr("bg_remove_model"))
        self._model_combo.setItemText(0, tr("bg_remove_model_general"))
        self._model_combo.setItemText(1, tr("bg_remove_model_human"))
        self._feather_label.setText(tr("bg_remove_feather"))
        self._info_label.setText(tr("bg_remove_png_note"))
        self._download_label.setText(tr("bg_remove_download_note"))
