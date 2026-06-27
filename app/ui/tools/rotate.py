from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QDial,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.models.tool_options import RotateOptions
from app.ui.tools.base_tool_widget import BaseToolWidget
from app.utils.i18n import tr


class RotateToolWidget(BaseToolWidget):
    def __init__(self) -> None:
        super().__init__()
        self._fill_color = QColor(255, 255, 255)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        angle_row = QHBoxLayout()
        self._angle_dial = QDial()
        self._angle_dial.setRange(0, 359)
        self._angle_dial.setNotchesVisible(True)
        self._angle_dial.setWrapping(True)
        self._angle_spin = QSpinBox()
        self._angle_spin.setRange(0, 359)
        self._angle_dial.valueChanged.connect(self._angle_spin.setValue)
        self._angle_spin.valueChanged.connect(self._angle_dial.setValue)
        self._angle_spin.valueChanged.connect(self._update_visibility)
        angle_row.addWidget(self._angle_dial)
        angle_row.addWidget(self._angle_spin)
        self._angle_label = QLabel()
        form.addRow(self._angle_label, angle_row)

        quick_row = QHBoxLayout()
        self._cw_btn = QPushButton()
        self._cw_btn.clicked.connect(lambda: self._adjust_angle(90))
        self._ccw_btn = QPushButton()
        self._ccw_btn.clicked.connect(lambda: self._adjust_angle(-90))
        self._flip180_btn = QPushButton()
        self._flip180_btn.clicked.connect(lambda: self._adjust_angle(180))
        quick_row.addWidget(self._cw_btn)
        quick_row.addWidget(self._ccw_btn)
        quick_row.addWidget(self._flip180_btn)
        self._quick_label = QLabel()
        form.addRow(self._quick_label, quick_row)

        self._flip_h_cb = QCheckBox()
        form.addRow(self._flip_h_cb)

        self._flip_v_cb = QCheckBox()
        form.addRow(self._flip_v_cb)

        self._auto_exif_cb = QCheckBox()
        self._auto_exif_cb.setChecked(True)
        form.addRow(self._auto_exif_cb)

        fill_row = QWidget()
        fill_layout = QHBoxLayout(fill_row)
        fill_layout.setContentsMargins(0, 0, 0, 0)
        self._fill_btn = QPushButton()
        self._fill_btn.setFixedSize(48, 28)
        self._fill_btn.clicked.connect(self._pick_fill_color)
        fill_layout.addWidget(self._fill_btn)
        fill_layout.addStretch(1)
        self._fill_label = QLabel()
        form.addRow(self._fill_label, fill_row)

        layout.addLayout(form)
        layout.addStretch(1)

        self._update_fill_btn_style()
        self._update_visibility()
        self.retranslate()

    def get_options(self) -> RotateOptions:
        return RotateOptions(
            angle=self._angle_spin.value(),
            flip_h=self._flip_h_cb.isChecked(),
            flip_v=self._flip_v_cb.isChecked(),
            auto_exif=self._auto_exif_cb.isChecked(),
            fill_color=(
                self._fill_color.red(),
                self._fill_color.green(),
                self._fill_color.blue(),
            ),
        )

    def retranslate(self) -> None:
        self._angle_label.setText(tr("rotate_angle"))
        self._quick_label.setText(tr("rotate_quick"))
        self._cw_btn.setText(tr("rotate_90_cw"))
        self._ccw_btn.setText(tr("rotate_90_ccw"))
        self._flip180_btn.setText(tr("rotate_180"))
        self._flip_h_cb.setText(tr("rotate_flip_h"))
        self._flip_v_cb.setText(tr("rotate_flip_v"))
        self._auto_exif_cb.setText(tr("rotate_auto_exif"))
        self._fill_label.setText(tr("rotate_fill_color"))
        self._fill_btn.setText(tr("convert_pick_color"))

    def _adjust_angle(self, delta: int) -> None:
        self._angle_spin.setValue((self._angle_spin.value() + delta) % 360)

    def _update_visibility(self) -> None:
        show_fill = self._angle_spin.value() != 0
        self._fill_label.setVisible(show_fill)
        self._fill_btn.setVisible(show_fill)

    def _pick_fill_color(self) -> None:
        color = QColorDialog.getColor(self._fill_color, self, tr("rotate_fill_color"))
        if color.isValid():
            self._fill_color = color
            self._update_fill_btn_style()

    def _update_fill_btn_style(self) -> None:
        self._fill_btn.setStyleSheet(
            f"background-color: {self._fill_color.name()}; border: 1px solid #888;"
        )
