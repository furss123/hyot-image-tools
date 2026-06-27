from PyQt6.QtWidgets import QWidget


class BaseToolWidget(QWidget):
    def get_options(self):
        raise NotImplementedError

    def validate(self) -> str | None:
        return None

    def retranslate(self) -> None:
        pass
