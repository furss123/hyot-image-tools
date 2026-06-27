from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.models.tool_options import CropOptions
from app.ui.tools.base_tool_widget import BaseToolWidget
from app.utils.i18n import tr

_PRESET_RATIOS = ("1:1", "4:3", "16:9", "3:4", "9:16")


class CropToolWidget(BaseToolWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._mode_combo = QComboBox()
        self._mode_combo.addItem("", "manual")
        self._mode_combo.addItem("", "ratio")
        self._mode_combo.addItem("", "center")
        self._mode_label = QLabel()
        form.addRow(self._mode_label, self._mode_combo)

        self._manual_widget = QWidget()
        manual_layout = QHBoxLayout(self._manual_widget)
        manual_layout.setContentsMargins(0, 0, 0, 0)
        self._x_spin = QSpinBox()
        self._x_spin.setRange(0, 32000)
        self._y_spin = QSpinBox()
        self._y_spin.setRange(0, 32000)
        self._w_spin = QSpinBox()
        self._w_spin.setRange(1, 32000)
        self._w_spin.setValue(800)
        self._h_spin = QSpinBox()
        self._h_spin.setRange(1, 32000)
        self._h_spin.setValue(600)
        self._x_label = QLabel()
        self._y_label = QLabel()
        self._w_label = QLabel()
        self._h_label = QLabel()
        manual_layout.addWidget(self._x_label)
        manual_layout.addWidget(self._x_spin)
        manual_layout.addWidget(self._y_label)
        manual_layout.addWidget(self._y_spin)
        manual_layout.addWidget(self._w_label)
        manual_layout.addWidget(self._w_spin)
        manual_layout.addWidget(self._h_label)
        manual_layout.addWidget(self._h_spin)
        self._manual_row_label = QLabel()
        form.addRow(self._manual_row_label, self._manual_widget)

        self._ratio_widget = QWidget()
        ratio_layout = QHBoxLayout(self._ratio_widget)
        ratio_layout.setContentsMargins(0, 0, 0, 0)
        self._ratio_combo = QComboBox()
        for ratio in _PRESET_RATIOS:
            self._ratio_combo.addItem(ratio, ratio)
        self._ratio_custom = QLineEdit()
        self._ratio_custom.setPlaceholderText("W:H")
        ratio_layout.addWidget(self._ratio_combo)
        ratio_layout.addWidget(self._ratio_custom, 1)
        self._ratio_label = QLabel()
        form.addRow(self._ratio_label, self._ratio_widget)

        layout.addLayout(form)
        layout.addStretch(1)

        self._mode_combo.currentIndexChanged.connect(self._update_visibility)
        self._update_visibility()
        self.retranslate()

    def get_options(self) -> CropOptions:
        custom_ratio = self._ratio_custom.text().strip()
        ratio = custom_ratio if custom_ratio else self._ratio_combo.currentData()
        return CropOptions(
            mode=self._mode_combo.currentData(),
            x=self._x_spin.value(),
            y=self._y_spin.value(),
            width=self._w_spin.value(),
            height=self._h_spin.value(),
            ratio=ratio,
        )

    def retranslate(self) -> None:
        self._mode_label.setText(tr("crop_mode"))
        self._mode_combo.setItemText(0, tr("crop_mode_manual"))
        self._mode_combo.setItemText(1, tr("crop_mode_ratio"))
        self._mode_combo.setItemText(2, tr("crop_mode_center"))
        self._manual_row_label.setText(tr("crop_manual"))
        self._x_label.setText(tr("crop_x"))
        self._y_label.setText(tr("crop_y"))
        self._w_label.setText(tr("crop_w"))
        self._h_label.setText(tr("crop_h"))
        self._ratio_label.setText(tr("crop_ratio"))

    def _update_visibility(self) -> None:
        mode = self._mode_combo.currentData()
        self._manual_widget.setVisible(mode == "manual")
        self._manual_row_label.setVisible(mode == "manual")
        self._ratio_widget.setVisible(mode == "ratio")
        self._ratio_label.setVisible(mode == "ratio")
