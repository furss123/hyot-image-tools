import ctypes
import sys

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "HyoT.ImageTools.1.0"
    )

from PyQt6.QtCore import QElapsedTimer, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from app.settings import load_settings
from app.ui.main_window import MainWindow
from app.ui.splash import SplashScreen
from app.utils.i18n import load

_ICON_PATH = "app/assets/icon.ico"


def main() -> None:
    app = QApplication(sys.argv)
    app_icon = QIcon(_ICON_PATH)
    app.setWindowIcon(app_icon)
    settings = load_settings()
    load(settings.language)

    splash = SplashScreen()
    splash.show()
    app.processEvents()

    elapsed = QElapsedTimer()
    elapsed.start()
    window = MainWindow(settings)
    window.setWindowIcon(app_icon)

    def show_main() -> None:
        window.show()
        splash.finish(window)

    QTimer.singleShot(max(0, 2000 - elapsed.elapsed()), show_main)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
