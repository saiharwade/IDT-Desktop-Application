import os
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QLineEdit,
    QPushButton,
    QSizePolicy,
)


class ClickableLabel(QLabel):
    def __init__(self, text="", url="", parent=None):
        super().__init__(text, parent)
        self.url = url
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if self.url:
            webbrowser.open(self.url)


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def create_input_field(self, placeholder, icon_text):
        field_frame = QFrame()
        field_frame.setObjectName("inputField")
        field_frame.setFixedHeight(64)
        field_frame.setStyleSheet("""
            QFrame#inputField {
                background-color: rgba(255, 255, 255, 0.88);
                border: 2px solid #efcb4c;
                border-radius: 18px;
            }
        """)

        field_layout = QHBoxLayout(field_frame)
        field_layout.setContentsMargins(18, 0, 18, 0)
        field_layout.setSpacing(12)

        icon_label = QLabel(icon_text)
        icon_label.setFixedWidth(28)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            color: #b2b2b2;
            font-size: 20px;
            border: none;
            background: transparent;
        """)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("""
            QLineEdit {
                border: none;
                background: transparent;
                color: #4c4c4c;
                font-size: 16px;
                padding: 0px;
            }
        """)

        field_layout.addWidget(icon_label)
        field_layout.addWidget(line_edit)

        return field_frame, line_edit

    def setup_ui(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "assets", "images", "logo.jpeg")
        bg_path = os.path.join(base_dir, "assets", "images", "background.png")

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setLayout(root_layout)

        self.bg_label = QLabel()
        self.bg_label.setScaledContents(True)

        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path))
        else:
            self.bg_label.setStyleSheet("background-color: #efe7d5;")

        root_layout.addWidget(self.bg_label)

        self.overlay = QWidget(self.bg_label)
        self.overlay.setStyleSheet("background: transparent;")

        main_layout = QHBoxLayout(self.overlay)
        main_layout.setContentsMargins(0, 0, 90, 0)
        main_layout.setSpacing(0)

        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        right_container = QWidget()
        right_container.setFixedWidth(760)

        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        right_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedSize(700, 820)
        card.setStyleSheet("""
            QFrame#loginCard {
                background-color: rgba(255, 255, 255, 0.35);
                border: 3px solid #efcb4c;
                border-radius: 38px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(78, 38, 78, 34)
        card_layout.setSpacing(0)
        card_layout.setAlignment(Qt.AlignTop)

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFixedHeight(150)
        logo_label.setStyleSheet("background: transparent; border: none;")

        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(
                logo_pixmap.scaled(
                    150,
                    150,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            logo_label.setText("IDT LOGO")
            logo_label.setStyleSheet("""
                color: #333333;
                font-size: 28px;
                font-weight: bold;
                border: none;
                background: transparent;
            """)

        title = QLabel("D-SCAN LOGIN")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("""
            color: #000000;
            border: none;
            background: transparent;
        """)

        subtitle = QLabel("Welcome back! Please enter you details")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: #1f1f1f;
            font-size: 22px;
            border: none;
            background: transparent;
        """)

        user_label = QLabel("UserID:")
        user_label.setStyleSheet("""
            color: #111111;
            font-size: 20px;
            font-weight: 500;
            background: transparent;
            border: none;
        """)

        user_field, self.user_input = self.create_input_field("Enter User ID", "👤")

        password_label = QLabel("Password:")
        password_label.setStyleSheet("""
            color: #111111;
            font-size: 20px;
            font-weight: 500;
            background: transparent;
            border: none;
        """)

        password_field, self.password_input = self.create_input_field("Enter Password", "🔒")
        self.password_input.setEchoMode(QLineEdit.Password)

        forgot_row = QWidget()
        forgot_row.setStyleSheet("background: transparent;")
        forgot_layout = QHBoxLayout(forgot_row)
        forgot_layout.setContentsMargins(0, 4, 0, 0)
        forgot_layout.setSpacing(0)

        forgot_spacer = QWidget()
        forgot_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        forgot_label = QLabel("Forget password?")
        forgot_label.setStyleSheet("""
            color: #2f2f2f;
            font-size: 11px;
            background: transparent;
            border: none;
        """)

        forgot_layout.addWidget(forgot_spacer)
        forgot_layout.addWidget(forgot_label)

        self.login_button = QPushButton("LOGIN")
        self.login_button.setFixedSize(360, 86)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                color: #000000;
                border: none;
                border-radius: 22px;
                font-size: 34px;
                font-weight: 700;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #efcc4f,
                    stop:1 #f0d45e
                );
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e6c03e,
                    stop:1 #edcf53
                );
            }
            QPushButton:pressed {
                background-color: #dfbb38;
            }
        """)

        login_button_wrap = QWidget()
        login_button_wrap.setStyleSheet("background: transparent;")
        login_button_layout = QHBoxLayout(login_button_wrap)
        login_button_layout.setContentsMargins(0, 0, 0, 0)
        login_button_layout.setAlignment(Qt.AlignCenter)
        login_button_layout.addWidget(self.login_button)

        social_widget = QWidget()
        social_widget.setStyleSheet("background: transparent;")
        social_layout = QHBoxLayout(social_widget)
        social_layout.setContentsMargins(0, 0, 0, 0)
        social_layout.setSpacing(16)
        social_layout.setAlignment(Qt.AlignCenter)

        fb = ClickableLabel("f", "https://facebook.com/yourpage")
        fb.setAlignment(Qt.AlignCenter)
        fb.setFixedSize(42, 42)
        fb.setStyleSheet("""
            QLabel {
                background-color: #efcc4f;
                color: #000000;
                font-size: 22px;
                font-weight: bold;
                border-radius: 10px;
            }
        """)

        ig = ClickableLabel("◎", "https://instagram.com/yourpage")
        ig.setAlignment(Qt.AlignCenter)
        ig.setFixedSize(42, 42)
        ig.setStyleSheet("""
            QLabel {
                background-color: #efcc4f;
                color: #000000;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
            }
        """)

        tw = ClickableLabel("𝕏", "https://x.com/yourpage")
        tw.setAlignment(Qt.AlignCenter)
        tw.setFixedSize(42, 42)
        tw.setStyleSheet("""
            QLabel {
                background-color: #efcc4f;
                color: #000000;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
            }
        """)

        social_layout.addWidget(fb)
        social_layout.addWidget(ig)
        social_layout.addWidget(tw)

        dots_widget = QWidget()
        dots_widget.setStyleSheet("background: transparent;")
        dots_layout = QHBoxLayout(dots_widget)
        dots_layout.setContentsMargins(0, 0, 0, 0)
        dots_layout.setSpacing(16)
        dots_layout.setAlignment(Qt.AlignCenter)

        for _ in range(3):
            dot = QLabel()
            dot.setFixedSize(14, 14)
            dot.setStyleSheet("""
                background-color: rgba(180, 170, 155, 0.95);
                border-radius: 7px;
            """)
            dots_layout.addWidget(dot)

        card_layout.addWidget(logo_label)
        card_layout.addSpacing(28)
        card_layout.addWidget(title)
        card_layout.addSpacing(8)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(54)
        card_layout.addWidget(user_label)
        card_layout.addSpacing(12)
        card_layout.addWidget(user_field)
        card_layout.addSpacing(42)
        card_layout.addWidget(password_label)
        card_layout.addSpacing(12)
        card_layout.addWidget(password_field)
        card_layout.addWidget(forgot_row)
        card_layout.addSpacing(34)
        card_layout.addWidget(login_button_wrap)
        card_layout.addSpacing(24)
        card_layout.addWidget(social_widget)
        card_layout.addSpacing(18)
        card_layout.addWidget(dots_widget)
        card_layout.addStretch()

        right_layout.addWidget(card)
        main_layout.addWidget(left_spacer, 1)
        main_layout.addWidget(right_container, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "bg_label"):
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
        if hasattr(self, "overlay"):
            self.overlay.setGeometry(0, 0, self.width(), self.height())