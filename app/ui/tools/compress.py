from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)

from app.models.tool_options import CompressOptions
from app.ui.tools.base_tool_widget import BaseToolWidget
from app.utils.i18n import tr


class CompressToolWidget(BaseToolWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        quality_row = QHBoxLayout()
        self._quality_slider = QSlider(Qt.Orientation.Horizontal)
        self._quality_slider.setRange(1, 100)
        self._quality_slider.setValue(85)
        self._quality_spin = QSpinBox()
        self._quality_spin.setRange(1, 100)
        self._quality_spin.setValue(85)
        self._quality_slider.valueChanged.connect(self._quality_spin.setValue)
        self._quality_spin.valueChanged.connect(self._quality_slider.setValue)
        quality_row.addWidget(self._quality_slider, 1)
        quality_row.addWidget(self._quality_spin)
        self._quality_label = QLabel()
        form.addRow(self._quality_label, quality_row)

        self._target_edit = QLineEdit("0")
        self._target_label = QLabel()
        form.addRow(self._target_label, self._target_edit)

        self._keep_format_cb = QCheckBox()
        self._keep_format_cb.setChecked(True)
        form.addRow(self._keep_format_cb)

        layout.addLayout(form)
        layout.addStretch(1)
        self.retranslate()

    def get_options(self) -> CompressOptions:
        try:
            target_kb = int(self._target_edit.text().strip() or "0")
        except ValueError:
            target_kb = 0
        return CompressOptions(
            quality=self._quality_spin.value(),
            target_kb=max(0, target_kb),
            keep_format=self._keep_format_cb.isChecked(),
        )

    def validate(self) -> str | None:
        if self._quality_spin.value() > 0:
            return None
        return tr("compress_quality_invalid")

    def retranslate(self) -> None:
        self._quality_label.setText(tr("compress_quality"))
        self._target_label.setText(tr("compress_target_kb"))
        self._target_edit.setPlaceholderText("0")
        self._keep_format_cb.setText(tr("compress_keep_format"))
