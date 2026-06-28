from PyQt6.QtWidgets import QWidget


class LogPanel(QWidget):
    """Deprecated — kept for import compatibility. Not shown in UI."""

    def __init__(self) -> None:
        super().__init__()
        self.hide()
        self.setFixedHeight(0)

    def append(self, msg: str) -> None:
        pass

    def update_count(self, n: int) -> None:
        pass

    def clear(self) -> None:
        pass

    def retranslate(self) -> None:
        pass
