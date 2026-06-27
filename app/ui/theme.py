DARK = {
    "accent": "#0078D4",
    "bg_base": "#0A0A0A",
    "bg_surface": "#1A1A1A",
    "text_primary": "#F0F0F0",
    "text_secondary": "#A0A0A0",
    "radius_md": "8px",
    "radius_lg": "12px",
    "radius_xl": "16px",
}

LIGHT = {
    "accent": "#0078D4",
    "bg_base": "#F3F3F3",
    "bg_surface": "#FFFFFF",
    "text_primary": "#1A1A1A",
    "text_secondary": "#5A5A5A",
    "radius_md": "8px",
    "radius_lg": "12px",
    "radius_xl": "16px",
}


def get_stylesheet(theme: str) -> str:
    t = LIGHT if theme == "light" else DARK
    return f"""
QWidget {{
    background-color: {t["bg_base"]};
    color: {t["text_primary"]};
    font-size: 13px;
}}

QPushButton {{
    background-color: {t["bg_surface"]};
    color: {t["text_primary"]};
    border: 1px solid {t["text_secondary"]};
    border-radius: {t["radius_md"]};
    padding: 6px 14px;
    min-height: 28px;
}}

QPushButton:hover {{
    border-color: {t["accent"]};
}}

QPushButton:pressed {{
    background-color: {t["bg_base"]};
}}

QPushButton:disabled {{
    color: {t["text_secondary"]};
    border-color: {t["bg_surface"]};
}}

QPushButton#primary {{
    background-color: {t["accent"]};
    color: #FFFFFF;
    border: none;
}}

QPushButton#primary:hover {{
    background-color: #106EBE;
}}

QPushButton#primary:pressed {{
    background-color: #005A9E;
}}

QPushButton#primary:disabled {{
    background-color: {t["bg_surface"]};
    color: {t["text_secondary"]};
}}

QLabel {{
    background-color: transparent;
    color: {t["text_primary"]};
}}

QListWidget {{
    background-color: {t["bg_surface"]};
    color: {t["text_primary"]};
    border: 1px solid {t["text_secondary"]};
    border-radius: {t["radius_lg"]};
    padding: 4px;
    outline: none;
}}

QListWidget::item {{
    padding: 6px 8px;
    border-radius: {t["radius_md"]};
}}

QListWidget::item:selected {{
    background-color: {t["accent"]};
    color: #FFFFFF;
}}

QListWidget::item:hover:!selected {{
    background-color: {t["bg_base"]};
}}

QLineEdit {{
    background-color: {t["bg_surface"]};
    color: {t["text_primary"]};
    border: 1px solid {t["text_secondary"]};
    border-radius: {t["radius_md"]};
    padding: 6px 10px;
    min-height: 28px;
    selection-background-color: {t["accent"]};
    selection-color: #FFFFFF;
}}

QLineEdit:focus {{
    border-color: {t["accent"]};
}}

QLineEdit:disabled {{
    color: {t["text_secondary"]};
    background-color: {t["bg_base"]};
}}

QProgressBar {{
    background-color: {t["bg_surface"]};
    border: 1px solid {t["text_secondary"]};
    border-radius: {t["radius_md"]};
    text-align: center;
    color: {t["text_primary"]};
    min-height: 20px;
}}

QProgressBar::chunk {{
    background-color: {t["accent"]};
    border-radius: {t["radius_md"]};
}}

QScrollBar:vertical {{
    background: {t["bg_base"]};
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {t["text_secondary"]};
    border-radius: 5px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background: {t["accent"]};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background: {t["bg_base"]};
    height: 10px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: {t["text_secondary"]};
    border-radius: 5px;
    min-width: 24px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {t["accent"]};
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0;
}}
""".strip()
