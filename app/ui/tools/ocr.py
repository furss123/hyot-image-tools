from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from app.models.tool_options import OcrOptions
from app.ui.tools.base_tool_widget import BaseToolWidget
from app.utils.i18n import tr

_LANGUAGES = (
    ("kor", "ocr_lang_kor"),
    ("eng", "ocr_lang_eng"),
    ("jpn", "ocr_lang_jpn"),
    ("chi_sim", "ocr_lang_chi_sim"),
)

_DEFAULT_LANGS = {"kor", "eng"}


class OcrToolWidget(BaseToolWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._lang_list = QListWidget()
        self._lang_list.setMaximumHeight(140)
        for code, _ in _LANGUAGES:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, code)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            state = (
                Qt.CheckState.Checked
                if code in _DEFAULT_LANGS
                else Qt.CheckState.Unchecked
            )
            item.setCheckState(state)
            self._lang_list.addItem(item)
        self._lang_label = QLabel()
        form.addRow(self._lang_label, self._lang_list)

        self._merge_cb = QCheckBox()
        form.addRow(self._merge_cb)

        layout.addLayout(form)

        self._info_label = QLabel()
        self._info_label.setWordWrap(True)
        layout.addWidget(self._info_label)

        layout.addStretch(1)
        self.retranslate()

    def get_options(self) -> OcrOptions:
        languages: list[str] = []
        for row in range(self._lang_list.count()):
            item = self._lang_list.item(row)
            if item is not None and item.checkState() == Qt.CheckState.Checked:
                languages.append(item.data(Qt.ItemDataRole.UserRole))
        if not languages:
            languages = ["kor", "eng"]
        return OcrOptions(
            languages=languages,
            merge_output=self._merge_cb.isChecked(),
        )

    def retranslate(self) -> None:
        self._lang_label.setText(tr("ocr_languages"))
        for row, (code, key) in enumerate(_LANGUAGES):
            item = self._lang_list.item(row)
            if item is not None:
                item.setText(tr(key))
        self._merge_cb.setText(tr("ocr_merge_output"))
        self._info_label.setText(tr("ocr_tesseract_note"))
