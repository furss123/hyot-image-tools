from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QLabel, QListWidget, QListWidgetItem

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
        super().__init__(tr("ocr_title"), tr("ocr_desc"))
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
        self._opt_row(tr("ocr_languages"), self._lang_list)

        self._merge_cb = QCheckBox()
        self._layout.addWidget(self._merge_cb)

        self._info_label = QLabel()
        self._info_label.setObjectName("infoNote")
        self._info_label.setWordWrap(True)
        self._layout.addWidget(self._info_label)
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
        super().retranslate()
        self._update_header(tr("ocr_title"), tr("ocr_desc"))
        for row, (code, key) in enumerate(_LANGUAGES):
            item = self._lang_list.item(row)
            if item is not None:
                item.setText(tr(key))
        self._merge_cb.setText(tr("ocr_merge_output"))
        self._info_label.setText(tr("ocr_tesseract_note"))
