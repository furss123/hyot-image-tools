import sys

from PyQt6.QtWidgets import QApplication

from app.settings import load_settings
from app.ui.main_window import MainWindow
from app.utils.i18n import load


def main() -> None:
    app = QApplication(sys.argv)
    settings = load_settings()
    load(settings.language)
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
