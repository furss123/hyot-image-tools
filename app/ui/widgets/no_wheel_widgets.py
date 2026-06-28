from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QAbstractSpinBox, QComboBox, QDoubleSpinBox, QLineEdit, QSpinBox


class NoWheelSpinBox(QSpinBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

    def wheelEvent(self, e) -> None:
        e.ignore()

    def focusInEvent(self, e) -> None:
        super().focusInEvent(e)
        QTimer.singleShot(0, self.selectAll)

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        if e.position().x() < self.width() - 20:
            QTimer.singleShot(0, self.selectAll)


class NoWheelDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

    def wheelEvent(self, e) -> None:
        e.ignore()

    def focusInEvent(self, e) -> None:
        super().focusInEvent(e)
        QTimer.singleShot(0, self.selectAll)

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        if e.position().x() < self.width() - 20:
            QTimer.singleShot(0, self.selectAll)


class NoWheelComboBox(QComboBox):
    def wheelEvent(self, e) -> None:
        e.ignore()


class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, e) -> None:
        super().focusInEvent(e)
        QTimer.singleShot(0, self.selectAll)

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        QTimer.singleShot(0, self.selectAll)
