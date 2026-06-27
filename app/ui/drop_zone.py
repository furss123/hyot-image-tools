from __future__ import annotations

from pathlib import Path

from PIL import Image
from PyQt6.QtCore import QObject, QRunnable, Qt, QThreadPool, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.models.file_item import FileItem
from app.utils.i18n import tr

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
    ".gif",
}

_IMAGE_FILTER = ";;".join(
    [
        "Images (*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.tif *.gif)",
        "All Files (*)",
    ]
)


def _is_image_path(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def _mime_has_images(mime_data) -> bool:
    if not mime_data.hasUrls():
        return False
    return any(_is_image_path(Path(url.toLocalFile())) for url in mime_data.urls())


def _paths_from_mime(mime_data) -> list[Path]:
    paths: list[Path] = []
    for url in mime_data.urls():
        path = Path(url.toLocalFile())
        if _is_image_path(path):
            paths.append(path.resolve())
    return paths


def _collect_images_from_folder(folder: Path) -> list[Path]:
    found: set[Path] = set()
    for path in folder.rglob("*"):
        if _is_image_path(path):
            found.add(path.resolve())
    return sorted(found)


class _MetadataSignals(QObject):
    loaded = pyqtSignal(Path, int, int, str)


class _MetadataWorker(QRunnable):
    def __init__(self, path: Path, signals: _MetadataSignals) -> None:
        super().__init__()
        self._path = path
        self._signals = signals

    def run(self) -> None:
        width = 0
        height = 0
        fmt = ""
        try:
            with Image.open(self._path) as img:
                width, height = img.size
                fmt = (img.format or self._path.suffix.lstrip(".")).upper()
        except Exception:
            pass
        self._signals.loaded.emit(self._path, width, height, fmt)


class _DropLabel(QLabel):
    files_dropped = pyqtSignal(list)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(120)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if _mime_has_images(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if _mime_has_images(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        paths = _paths_from_mime(event.mimeData())
        if paths:
            self.files_dropped.emit(paths)
            event.acceptProposedAction()
        else:
            event.ignore()


class DropZone(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._files: list[FileItem] = []
        self._pool = QThreadPool.globalInstance()
        self._metadata_signals = _MetadataSignals()
        self._metadata_signals.loaded.connect(self._on_metadata_loaded)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._drop_label = _DropLabel()
        self._drop_label.files_dropped.connect(self.add_files)
        layout.addWidget(self._drop_label)

        button_row = QHBoxLayout()
        button_row.setSpacing(8)

        self._add_files_btn = QPushButton()
        self._add_files_btn.clicked.connect(self._browse_files)
        button_row.addWidget(self._add_files_btn)

        self._add_folder_btn = QPushButton()
        self._add_folder_btn.clicked.connect(self._browse_folder)
        button_row.addWidget(self._add_folder_btn)

        self._clear_btn = QPushButton()
        self._clear_btn.clicked.connect(self.clear)
        button_row.addWidget(self._clear_btn)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        self._table = QTableWidget(0, 4)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self._table, 1)

        self._apply_drop_style()
        self.retranslate()

    @property
    def files(self) -> list[FileItem]:
        return list(self._files)

    def add_files(self, paths: list[Path]) -> None:
        existing = {item.path for item in self._files}
        for raw in paths:
            path = Path(raw).resolve()
            if not _is_image_path(path) or path in existing:
                continue
            existing.add(path)
            item = FileItem(path=path)
            self._files.append(item)
            row = self._table.rowCount()
            self._table.insertRow(row)
            self._set_row_basic(row, item)
            self._queue_metadata(item)

    def clear(self) -> None:
        self._files.clear()
        self._table.setRowCount(0)

    def retranslate(self) -> None:
        self._drop_label.setText(tr("drop_hint"))
        self._add_files_btn.setText(tr("add_files"))
        self._add_folder_btn.setText(tr("add_folder"))
        self._clear_btn.setText(tr("clear"))
        self._table.setHorizontalHeaderLabels(
            [
                tr("col_filename"),
                tr("col_size"),
                tr("col_dimensions"),
                tr("col_format"),
            ]
        )

    def _apply_drop_style(self) -> None:
        self._drop_label.setStyleSheet(
            "QLabel {"
            "  border: 2px dashed #A0A0A0;"
            "  border-radius: 8px;"
            "  padding: 32px;"
            "  background: transparent;"
            "}"
        )

    def _browse_files(self) -> None:
        selected, _ = QFileDialog.getOpenFileNames(
            self,
            tr("add_files"),
            "",
            _IMAGE_FILTER,
        )
        if selected:
            self.add_files([Path(p) for p in selected])

    def _browse_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, tr("add_folder"))
        if folder:
            self.add_files(_collect_images_from_folder(Path(folder)))

    def _set_row_basic(self, row: int, item: FileItem) -> None:
        self._table.setItem(row, 0, QTableWidgetItem(item.filename))
        self._table.setItem(row, 1, QTableWidgetItem(f"{item.size_kb:.1f}"))
        self._table.setItem(row, 2, QTableWidgetItem("..."))
        self._table.setItem(row, 3, QTableWidgetItem("..."))

    def _queue_metadata(self, item: FileItem) -> None:
        worker = _MetadataWorker(item.path, self._metadata_signals)
        self._pool.start(worker)

    def _on_metadata_loaded(self, path: Path, width: int, height: int, fmt: str) -> None:
        item = next((f for f in self._files if f.path == path), None)
        if item is None:
            return

        if width > 0 and height > 0:
            item.width = width
            item.height = height
        if fmt:
            item.format = fmt

        row = self._files.index(item)
        if row >= self._table.rowCount():
            return

        if item.width and item.height:
            self._table.item(row, 2).setText(f"{item.width}x{item.height}")
        else:
            self._table.item(row, 2).setText("-")

        self._table.item(row, 3).setText(item.format or "-")
