from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from app.models.tool_options import ConvertOptions
from app.ui.tools.base_tool_widget import BaseToolWidget
from app.utils.i18n import tr


class ConvertToolWidget(BaseToolWidget):
    def __init__(self) -> None:
        super().__init__()
        self._bg_color = QColor(255, 255, 255)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._format_combo = QComboBox()
        for fmt in ("JPEG", "PNG", "WEBP", "BMP", "TIFF", "GIF", "ICO"):
            self._format_combo.addItem("", fmt)
        self._format_label = QLabel()
        form.addRow(self._format_label, self._format_combo)

        self._quality_spin = QSpinBox()
        self._quality_spin.setRange(1, 100)
        self._quality_spin.setValue(85)
        self._quality_label = QLabel()
        form.addRow(self._quality_label, self._quality_spin)

        bg_row = QHBoxLayout()
        self._bg_btn = QPushButton()
        self._bg_btn.setFixedSize(48, 28)
        self._bg_btn.clicked.connect(self._pick_bg_color)
        bg_row.addWidget(self._bg_btn)
        bg_row.addStretch(1)
        self._bg_label = QLabel()
        form.addRow(self._bg_label, bg_row)

        layout.addLayout(form)
        layout.addStretch(1)

        self._format_combo.currentIndexChanged.connect(self._update_visibility)
        self._update_bg_btn_style()
        self._update_visibility()
        self.retranslate()

    def get_options(self) -> ConvertOptions:
        return ConvertOptions(
            format=self._format_combo.currentData(),
            quality=self._quality_spin.value(),
            bg_color=(
                self._bg_color.red(),
                self._bg_color.green(),
                self._bg_color.blue(),
            ),
        )

    def retranslate(self) -> None:
        self._format_label.setText(tr("convert_format"))
        self._format_combo.setItemText(0, "JPG")
        self._format_combo.setItemText(1, "PNG")
        self._format_combo.setItemText(2, "WEBP")
        self._format_combo.setItemText(3, "BMP")
        self._format_combo.setItemText(4, "TIFF")
        self._format_combo.setItemText(5, "GIF")
        self._format_combo.setItemText(6, "ICO")
        self._quality_label.setText(tr("convert_quality"))
        self._bg_label.setText(tr("convert_bg_color"))
        self._bg_btn.setText(tr("convert_pick_color"))

    def _update_visibility(self) -> None:
        fmt = self._format_combo.currentData()
        show_quality = fmt in ("JPEG", "WEBP")
        self._quality_label.setVisible(show_quality)
        self._quality_spin.setVisible(show_quality)
        show_bg = fmt == "JPEG"
        self._bg_label.setVisible(show_bg)
        self._bg_btn.setVisible(show_bg)

    def _pick_bg_color(self) -> None:
        color = QColorDialog.getColor(self._bg_color, self, tr("convert_bg_color"))
        if color.isValid():
            self._bg_color = color
            self._update_bg_btn_style()

    def _update_bg_btn_style(self) -> None:
        self._bg_btn.setStyleSheet(
            f"background-color: {self._bg_color.name()}; border: 1px solid #888;"
        )
