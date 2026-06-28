from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel, QWidget


class Toast(QLabel):
    def __init__(self, parent: QWidget, message: str, success: bool = True) -> None:
        super().__init__(message, parent)
        color = "#4CAF50" if success else "#F44336"
        self.setStyleSheet(
            f"""
            background: {color};
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 13px;
        """
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjustSize()
        x = parent.width() - self.width() - 20
        y = parent.height() - self.height() - 60
        self.move(max(20, x), max(20, y))
        self.show()
        self.raise_()
        QTimer.singleShot(2500, self.hide)
