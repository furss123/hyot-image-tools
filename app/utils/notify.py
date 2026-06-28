import sys


def play_completion_sound(*, all_success: bool = True) -> None:
    try:
        if sys.platform == "win32":
            import winsound

            winsound.MessageBeep(
                winsound.MB_OK if all_success else winsound.MB_ICONEXCLAMATION
            )
        else:
            from PyQt6.QtWidgets import QApplication

            app = QApplication.instance()
            if app is not None:
                QApplication.beep()
    except Exception:
        pass
