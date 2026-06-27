from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.models.tool_options import ResizeOptions
from app.ui.tools.base_tool_widget import BaseToolWidget
from app.utils.i18n import tr


class ResizeToolWidget(BaseToolWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._mode_combo = QComboBox()
        self._mode_combo.addItem("", "percent")
        self._mode_combo.addItem("", "exact")
        self._mode_combo.addItem("", "longest_side")
        self._mode_label = QLabel()
        form.addRow(self._mode_label, self._mode_combo)

        self._percent_widget = QWidget()
        percent_layout = QHBoxLayout(self._percent_widget)
        percent_layout.setContentsMargins(0, 0, 0, 0)
        self._percent_spin = QSpinBox()
        self._percent_spin.setRange(1, 1000)
        self._percent_spin.setValue(100)
        self._percent_spin.setSuffix("%")
        percent_layout.addWidget(self._percent_spin)
        self._percent_label = QLabel()
        form.addRow(self._percent_label, self._percent_widget)

        self._exact_widget = QWidget()
        exact_layout = QHBoxLayout(self._exact_widget)
        exact_layout.setContentsMargins(0, 0, 0, 0)
        self._width_spin = QSpinBox()
        self._width_spin.setRange(1, 32000)
        self._width_spin.setValue(1920)
        self._height_spin = QSpinBox()
        self._height_spin.setRange(1, 32000)
        self._height_spin.setValue(1080)
        self._width_label = QLabel()
        self._height_label = QLabel()
        exact_layout.addWidget(self._width_label)
        exact_layout.addWidget(self._width_spin)
        exact_layout.addWidget(self._height_label)
        exact_layout.addWidget(self._height_spin)
        self._exact_row_label = QLabel()
        form.addRow(self._exact_row_label, self._exact_widget)

        self._keep_aspect_cb = QCheckBox()
        self._keep_aspect_cb.setChecked(True)
        form.addRow(self._keep_aspect_cb)

        self._longest_widget = QWidget()
        longest_layout = QHBoxLayout(self._longest_widget)
        longest_layout.setContentsMargins(0, 0, 0, 0)
        self._longest_spin = QSpinBox()
        self._longest_spin.setRange(1, 32000)
        self._longest_spin.setValue(1920)
        longest_layout.addWidget(self._longest_spin)
        self._longest_label = QLabel()
        form.addRow(self._longest_label, self._longest_widget)

        self._allow_upscale_cb = QCheckBox()
        form.addRow(self._allow_upscale_cb)

        self._resample_combo = QComboBox()
        self._resample_combo.addItem("", "lanczos")
        self._resample_combo.addItem("", "bicubic")
        self._resample_combo.addItem("", "nearest")
        self._resample_label = QLabel()
        form.addRow(self._resample_label, self._resample_combo)

        layout.addLayout(form)
        layout.addStretch(1)

        self._mode_combo.currentIndexChanged.connect(self._update_mode_visibility)
        self._update_mode_visibility()
        self.retranslate()

    def get_options(self) -> ResizeOptions:
        return ResizeOptions(
            mode=self._mode_combo.currentData(),
            percent=self._percent_spin.value(),
            width=self._width_spin.value(),
            height=self._height_spin.value(),
            keep_aspect=self._keep_aspect_cb.isChecked(),
            longest_side=self._longest_spin.value(),
            allow_upscale=self._allow_upscale_cb.isChecked(),
            resample=self._resample_combo.currentData(),
        )

    def retranslate(self) -> None:
        self._mode_label.setText(tr("resize_mode"))
        self._mode_combo.setItemText(0, tr("resize_mode_percent"))
        self._mode_combo.setItemText(1, tr("resize_mode_exact"))
        self._mode_combo.setItemText(2, tr("resize_mode_longest"))

        self._percent_label.setText(tr("resize_percent"))
        self._exact_row_label.setText(tr("resize_exact"))
        self._width_label.setText(tr("resize_width"))
        self._height_label.setText(tr("resize_height"))
        self._keep_aspect_cb.setText(tr("resize_keep_aspect"))
        self._longest_label.setText(tr("resize_longest_side"))
        self._allow_upscale_cb.setText(tr("resize_allow_upscale"))
        self._resample_label.setText(tr("resize_resample"))
        self._resample_combo.setItemText(0, tr("resize_resample_lanczos"))
        self._resample_combo.setItemText(1, tr("resize_resample_bicubic"))
        self._resample_combo.setItemText(2, tr("resize_resample_nearest"))

    def _update_mode_visibility(self) -> None:
        mode = self._mode_combo.currentData()
        self._percent_widget.setVisible(mode == "percent")
        self._percent_label.setVisible(mode == "percent")
        self._exact_widget.setVisible(mode == "exact")
        self._exact_row_label.setVisible(mode == "exact")
        self._keep_aspect_cb.setVisible(mode == "exact")
        self._longest_widget.setVisible(mode == "longest_side")
        self._longest_label.setVisible(mode == "longest_side")
