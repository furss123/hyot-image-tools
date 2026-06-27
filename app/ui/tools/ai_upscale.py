from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
)

from app.models.tool_options import AiUpscaleOptions
from app.ui.tools.base_tool_widget import BaseToolWidget
from app.utils.i18n import tr


class AiUpscaleToolWidget(BaseToolWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._scale_combo = QComboBox()
        self._scale_combo.addItem("2x", 2)
        self._scale_combo.addItem("4x", 4)
        self._scale_combo.setCurrentIndex(1)
        self._scale_label = QLabel()
        form.addRow(self._scale_label, self._scale_combo)

        self._model_combo = QComboBox()
        self._model_combo.addItem("", "realesrgan-x4plus")
        self._model_combo.addItem("", "realesrgan-x4plus-anime")
        self._model_label = QLabel()
        form.addRow(self._model_label, self._model_combo)

        layout.addLayout(form)

        self._binary_label = QLabel()
        self._binary_label.setWordWrap(True)
        layout.addWidget(self._binary_label)

        self._gpu_label = QLabel()
        self._gpu_label.setWordWrap(True)
        layout.addWidget(self._gpu_label)

        layout.addStretch(1)
        self.retranslate()

    def get_options(self) -> AiUpscaleOptions:
        return AiUpscaleOptions(
            scale=self._scale_combo.currentData(),
            model=self._model_combo.currentData(),
        )

    def retranslate(self) -> None:
        self._scale_label.setText(tr("ai_upscale_scale"))
        self._model_label.setText(tr("ai_upscale_model"))
        self._model_combo.setItemText(0, tr("ai_upscale_model_photo"))
        self._model_combo.setItemText(1, tr("ai_upscale_model_anime"))
        self._binary_label.setText(tr("ai_upscale_binary_note"))
        self._gpu_label.setText(tr("ai_upscale_gpu_note"))
