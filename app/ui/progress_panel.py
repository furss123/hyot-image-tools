from PyQt6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget


class ProgressPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._overall_bar = QProgressBar()
        self._overall_bar.setRange(0, 100)
        self._overall_bar.setValue(0)
        layout.addWidget(self._overall_bar)

        self._file_label = QLabel()
        layout.addWidget(self._file_label)

        self._file_bar = QProgressBar()
        self._file_bar.setRange(0, 100)
        self._file_bar.setValue(0)
        layout.addWidget(self._file_bar)

        self.reset()

    def update_file(self, filename: str, percent: int) -> None:
        self._file_label.setText(filename)
        self._file_bar.setValue(max(0, min(100, percent)))

    def update_overall(self, current: int, total: int) -> None:
        if total > 0:
            value = int(current * 100 / total)
            self._overall_bar.setValue(max(0, min(100, value)))
            self._overall_bar.setFormat(f"{current} / {total}")
        else:
            self._overall_bar.setValue(0)
            self._overall_bar.setFormat("")

    def reset(self) -> None:
        self._overall_bar.setValue(0)
        self._overall_bar.setFormat("")
        self._file_label.clear()
        self._file_bar.setValue(0)
