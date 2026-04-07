import os
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QPixmap, QPolygonF
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QFrame, QSizePolicy
)


class ImageLabel(QLabel):
    def __init__(self, image_path="", width=40, height=40, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: none; background: transparent;")
        self.set_image(image_path)

    def set_image(self, image_path):
        self.clear()
        self.setStyleSheet("border: none; background: transparent;")

        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    self.width(),
                    self.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.setPixmap(pixmap)
                return

        self.setText("◎")
        self.setStyleSheet("""
            QLabel {
                background-color: #E7C75D;
                border: 1px solid #CFAE47;
                border-radius: 17px;
                color: #111111;
                font-size: 15px;
                font-weight: 700;
            }
        """)


class StripeBar(QWidget):
    def __init__(self, filled=7, total=18, parent=None):
        super().__init__(parent)
        self.filled = filled
        self.total = total
        self.setFixedSize(180, 18)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gap = 2
        seg_w = 7
        seg_h = 14
        y = 2

        for i in range(self.total):
            x = i * (seg_w + gap)
            points = QPolygonF([
                QPointF(x, y + seg_h),
                QPointF(x + seg_w, y + seg_h - 2),
                QPointF(x + seg_w, y + 2),
                QPointF(x, y + 4)
            ])

            if i < self.filled:
                painter.setBrush(QColor("#D9B63A"))
                painter.setPen(QPen(QColor("#D9B63A"), 1))
            else:
                painter.setBrush(QColor("#F0F0F0"))
                painter.setPen(QPen(QColor("#CFCFCF"), 1))

            painter.drawPolygon(points)


class CompareViewBox(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #F2F2F2;
                border: 1px solid #DCC374;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 10)
        layout.setSpacing(0)

        title_label = QLabel(title)
        title_font = QFont("Segoe UI", 10)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #8A8A8A; border: none;")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        layout.addWidget(title_label)
        layout.addStretch()


class ComparePage(QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.analysis_visible = False
        self.setStyleSheet("background-color: #F8F8F8;")
        self.setup_ui()

    def go_home(self):
        if self.stacked_widget is not None:
            self.stacked_widget.setCurrentIndex(1)

    def toggle_advanced_analysis(self):
        self.analysis_visible = not self.analysis_visible
        self.bars_widget.setVisible(self.analysis_visible)

    def make_small_button(self, text, w=34, h=28):
        btn = QPushButton(text)
        btn.setFixedSize(w, h)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F8F8;
                border: 1px solid #DCC374;
                border-radius: 5px;
                color: #222222;
                font-family: Segoe UI;
                font-size: 10px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #FCFCFC;
            }
        """)
        return btn

    def make_action_button(self, text, w=110, h=30, font_size=10):
        btn = QPushButton(text)
        btn.setFixedSize(w, h)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #F8F8F8;
                border: 1px solid #DCC374;
                border-radius: 5px;
                color: #222222;
                font-family: Segoe UI;
                font-size: {font_size}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #FCFCFC;
            }}
        """)
        return btn

    def make_value_box(self, text="00", w=46, h=28):
        box = QLabel(text)
        box.setAlignment(Qt.AlignCenter)
        box.setFixedSize(w, h)
        box.setStyleSheet("""
            QLabel {
                background-color: #F8F8F8;
                border: 1px solid #DCC374;
                border-radius: 4px;
                color: #333333;
                font-family: Segoe UI;
                font-size: 10px;
            }
        """)
        return box

    def setup_ui(self):
        gold_border = "#DCC374"
        text_color = "#222222"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "..", "assets", "images", "logo.jpeg")
        logo_path = os.path.abspath(logo_path)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar
        top_bar = QFrame()
        top_bar.setFixedHeight(75)
        top_bar.setStyleSheet(f"""
            QFrame {{
                background-color: #F8F8F8;
                border-bottom: 1px solid {gold_border};
            }}
        """)

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(12, 10, 12, 10)
        top_layout.setSpacing(0)

        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        logo_circle = ImageLabel(logo_path, 32, 32)

        brand_text = QLabel("SYD-PRO")
        brand_font = QFont("Segoe UI", 16)
        brand_font.setBold(True)
        brand_text.setFont(brand_font)
        brand_text.setStyleSheet(f"color: {text_color};")

        left_layout.addWidget(logo_circle)
        left_layout.addWidget(brand_text)
        left_layout.addStretch()

        title = QLabel("COMPARE")
        title_font = QFont("Segoe UI", 16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {text_color};")

        right_space = QWidget()

        top_layout.addWidget(left_widget, 1)
        top_layout.addWidget(title, 1)
        top_layout.addWidget(right_space, 1)

        # Center
        center_frame = QFrame()
        center_frame.setStyleSheet("background-color: #F8F8F8;")
        center_layout = QHBoxLayout(center_frame)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        # Left compare area
        left_area = QWidget()
        left_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_grid = QGridLayout(left_area)
        left_grid.setContentsMargins(0, 0, 0, 0)
        left_grid.setSpacing(0)

        box1 = CompareViewBox("Result")
        box2 = CompareViewBox("Flourescence")
        box3 = CompareViewBox("Short Phosphorous")
        box4 = CompareViewBox("Long Phosphorous")

        left_grid.addWidget(box1, 0, 0)
        left_grid.addWidget(box2, 0, 1)
        left_grid.addWidget(box3, 1, 0)
        left_grid.addWidget(box4, 1, 1)

        # Right panel
        right_panel = QFrame()
        right_panel.setFixedWidth(570)
        right_panel.setStyleSheet(f"""
            QFrame {{
                background-color: #FAFAFA;
                border-left: 1px solid {gold_border};
            }}
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(22, 16, 22, 16)
        right_layout.setSpacing(12)

        # Logo block
        logo_row = QHBoxLayout()
        logo_row.setContentsMargins(0, 0, 0, 0)
        logo_row.setSpacing(8)

        company_logo = ImageLabel(logo_path, 52, 52)

        logo_top = QLabel("IDT")
        logo_top_font = QFont("Times New Roman", 34)
        logo_top.setFont(logo_top_font)
        logo_top.setStyleSheet("color: #3C2B22; border: none;")

        logo_row.addStretch()
        logo_row.addWidget(company_logo)
        logo_row.addWidget(logo_top)
        logo_row.addStretch()

        logo_widget = QWidget()
        logo_widget.setLayout(logo_row)

        logo_sub = QLabel("IDT GEMOLOGICAL LABORATORIES WORLDWIDE")
        logo_sub_font = QFont("Segoe UI", 6)
        logo_sub.setFont(logo_sub_font)
        logo_sub.setAlignment(Qt.AlignCenter)
        logo_sub.setStyleSheet("color: #111111; border: none;")

        right_layout.addWidget(logo_widget)
        right_layout.addWidget(logo_sub)

        # Inputs - refined
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setContentsMargins(20, 12, 20, 0)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(16)

        label_font = QFont("Segoe UI", 12)
        input_font = QFont("Segoe UI", 12)

        for row, txt in enumerate(["HPHT:", "CVD:"]):
            lab = QLabel(txt)
            lab.setFont(label_font)
            lab.setStyleSheet("color: #333333; border: none;")

            inp = QLineEdit()
            inp.setFont(input_font)
            inp.setFixedHeight(32)
            inp.setStyleSheet(f"""
                QLineEdit {{
                    background: #F8F8F8;
                    border: 1px solid {gold_border};
                    border-radius: 5px;
                    padding-left: 10px;
                    color: #222222;
                }}
            """)

            form_layout.addWidget(lab, row, 0, alignment=Qt.AlignLeft)
            form_layout.addWidget(inp, row, 1)

        right_layout.addWidget(form_widget)

        # + 00 -
        step_row = QHBoxLayout()
        step_row.setContentsMargins(0, 10, 0, 0)
        step_row.setSpacing(12)
        step_row.setAlignment(Qt.AlignCenter)

        plus_btn = self.make_small_button("+", 30, 28)
        minus_btn = self.make_small_button("−", 30, 28)
        value_box = self.make_value_box("00", 46, 28)

        step_row.addWidget(plus_btn)
        step_row.addWidget(value_box)
        step_row.addWidget(minus_btn)

        right_layout.addLayout(step_row)

        # High gain / Simulant
        row_btns = QHBoxLayout()
        row_btns.setContentsMargins(0, 10, 0, 0)
        row_btns.setSpacing(18)
        row_btns.setAlignment(Qt.AlignCenter)

        high_gain_btn = self.make_action_button("High gain", 110, 28, 9)
        simulant_btn = self.make_action_button("Simulant", 100, 28, 9)

        row_btns.addWidget(high_gain_btn)
        row_btns.addWidget(simulant_btn)

        right_layout.addLayout(row_btns)

        # Advance Analysis
        adv_btn = self.make_action_button("Advance Analysis", 150, 30, 9)
        adv_btn.clicked.connect(self.toggle_advanced_analysis)
        adv_wrap = QHBoxLayout()
        adv_wrap.setContentsMargins(0, 6, 0, 0)
        adv_wrap.setAlignment(Qt.AlignCenter)
        adv_wrap.addWidget(adv_btn)

        right_layout.addLayout(adv_wrap)

        # Bars
        self.bars_widget = QWidget()
        bars_layout = QGridLayout(self.bars_widget)
        bars_layout.setContentsMargins(60, 10, 60, 0)
        bars_layout.setHorizontalSpacing(18)
        bars_layout.setVerticalSpacing(12)

        bar_labels = ["Gain:", "Exposer:", "Shutter:", "ISO:"]
        fills = [7, 6, 5, 5]

        for i, (txt, fill) in enumerate(zip(bar_labels, fills)):
            lab = QLabel(txt)
            lab.setFont(QFont("Segoe UI", 10))
            lab.setStyleSheet("color: #333333; border: none;")

            bar = StripeBar(fill)

            bars_layout.addWidget(lab, i, 0)
            bars_layout.addWidget(bar, i, 1)

        self.bars_widget.setVisible(False)
        right_layout.addWidget(self.bars_widget)
        right_layout.addStretch()

        # Bottom nav buttons
        nav_row = QHBoxLayout()
        nav_row.setContentsMargins(40, 0, 40, 0)
        nav_row.setSpacing(16)

        home_btn = self.make_action_button("Home", 72, 28, 9)
        result_btn = self.make_action_button("Result", 72, 28, 9)
        cert_btn = self.make_action_button("Certificate", 100, 28, 9)

        home_btn.clicked.connect(self.go_home)

        nav_row.addStretch()
        nav_row.addWidget(home_btn)
        nav_row.addWidget(result_btn)
        nav_row.addWidget(cert_btn)
        nav_row.addStretch()

        right_layout.addLayout(nav_row)

        center_layout.addWidget(left_area, 1)
        center_layout.addWidget(right_panel, 0)

        # Footer
        footer = QFrame()
        footer.setFixedHeight(48)
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: #F8F8F8;
                border-top: 1px solid {gold_border};
            }}
        """)

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(24, 6, 24, 6)

        footer_left = QLabel("IDT Gemological Laboratories Worldwide")
        footer_right = QLabel("www.idtworldwide.com")

        footer_font = QFont("Segoe UI", 12)
        footer_font.setBold(True)
        footer_left.setFont(footer_font)
        footer_right.setFont(footer_font)

        footer_left.setStyleSheet("color: #111111;")
        footer_right.setStyleSheet("color: #111111;")

        footer_layout.addWidget(footer_left)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_right)

        main_layout.addWidget(top_bar)
        main_layout.addWidget(center_frame)
        main_layout.addWidget(footer)
