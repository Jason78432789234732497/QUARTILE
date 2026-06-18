import sys
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Colors from your Affinity theme
APP_BG = "#4981ff"        # browser bg / titlebar
URL_BG = "#8eb1ff"        # url bar bg
TEXT_FG = "#000000"
BTN_CLOSE_TOP = "#ff6d6d"
BTN_CLOSE_BOTTOM = "#ff4b5d"
ICON_FG = "#ffffff"

BASE_FONT_FAMILY = "Lucida Grande"
BASE_FONT_SIZE = 11


class LuxChromiumBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Frameless, fixed-size window (like Tkinter overrideredirect + resizable(False, False))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(900, 600)

        self._drag_pos = QPoint()

        app_font = QFont(BASE_FONT_FAMILY, BASE_FONT_SIZE)
        self.setFont(app_font)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----- Custom title bar -----
        title_bar = QWidget()
        title_bar.setStyleSheet(f"background-color: {APP_BG};")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 4, 10, 4)
        title_layout.setSpacing(8)

        self.title_label = QLabel("Krystasis Browser")
        self.title_label.setFont(QFont(BASE_FONT_FAMILY, BASE_FONT_SIZE, QFont.Bold))
        self.title_label.setStyleSheet(f"color: {TEXT_FG};")

        self.close_btn = QPushButton("✕")
        self.close_btn.setFont(app_font)
        self.close_btn.setFixedHeight(20)
        self.close_btn.setStyleSheet(
            f"""
            QPushButton {{
                color: {ICON_FG};
                border: none;
                padding: 0 10px;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {BTN_CLOSE_TOP},
                    stop:1 {BTN_CLOSE_BOTTOM}
                );
            }}
            QPushButton:hover {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff8a8a,
                    stop:1 #ff6b6b
                );
            }}
            """
        )
        self.close_btn.clicked.connect(self.close)

        title_layout.addWidget(self.title_label)
        title_layout.addStretch(1)
        title_layout.addWidget(self.close_btn)

        # ----- Toolbar (like old Tkinter: ← → ⟳ URL Go) -----
        toolbar = QWidget()
        toolbar.setStyleSheet(f"background-color: {APP_BG};")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(10, 5, 10, 5)
        tb_layout.setSpacing(8)

        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.reload_btn = QPushButton("⟳")
        for btn in (self.back_btn, self.forward_btn, self.reload_btn):
            btn.setFont(app_font)
            btn.setFixedWidth(32)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {APP_BG};
                    color: {TEXT_FG};
                    border: none;
                    padding: 4px 0;
                }}
                QPushButton:hover {{
                    background-color: #ffffff33;
                }}
                """
            )

        self.urlbar = QLineEdit()
        self.urlbar.setFont(app_font)
        self.urlbar.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {URL_BG};
                color: {TEXT_FG};
                border: none;
                padding: 4px 8px;
            }}
            """
        )
        self.urlbar.setText("https://raindeco.neocities.com")

        self.go_btn = QPushButton("Go")
        self.go_btn.setFont(app_font)
        self.go_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {URL_BG};
                color: {TEXT_FG};
                border: none;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: #ffffff66;
            }}
            """
        )

        tb_layout.addWidget(self.back_btn)
        tb_layout.addWidget(self.forward_btn)
        tb_layout.addWidget(self.reload_btn)
        tb_layout.addWidget(self.urlbar, 1)
        tb_layout.addWidget(self.go_btn)

        # ----- Web view (Chromium) -----
        self.web = QWebEngineView()
        self.web.setUrl(QUrl(self.urlbar.text()))

        main_layout.addWidget(title_bar)
        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.web)

        # Wire up actions
        self.go_btn.clicked.connect(self.load_url)
        self.urlbar.returnPressed.connect(self.load_url)
        self.back_btn.clicked.connect(self.web.back)
        self.forward_btn.clicked.connect(self.web.forward)
        self.reload_btn.clicked.connect(self.web.reload)

    # ----- Dragging the frameless window -----
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    # ----- URL loading -----
    def load_url(self):
        url = self.urlbar.text().strip()
        if not url:
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.web.setUrl(QUrl(url))


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont(BASE_FONT_FAMILY, BASE_FONT_SIZE))
    win = LuxChromiumBrowser()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
