import sys
import os
import math
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import (
    QFont, QColor, QPainter, QPen, QPixmap,
    QPainterPath, QPolygonF
)
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QFrame,
    QSizePolicy,
    QDesktopWidget,
    QSlider
)


class SpinnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(90, 90)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = 26

        for i in range(12):
            angle = i * 30
            painter.save()
            painter.translate(center_x, center_y)
            painter.rotate(angle)

            alpha = 30 + (i * 18)
            color = QColor(0, 0, 0, min(alpha, 255))
            pen = QPen(color, 5, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(0, -radius, 0, -(radius + 11))
            painter.restore()


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


class SymbolButton(QPushButton):
    def __init__(self, kind="generic", has_arrow=False, parent=None):
        super().__init__(parent)
        self.kind = kind
        self.has_arrow = has_arrow
        # Match Figma Desktop-3 icon tile (60 x 61)
        self.setFixedSize(60, 61)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Figma style: flat golden tile with inset shadow and small radius.
        outer = QRectF(0.5, 0.5, self.width() - 1, self.height() - 2)
        # base fill
        painter.setPen(QPen(QColor("#EDC84A"), 1))
        painter.setBrush(QColor("#FFE693"))
        painter.drawRoundedRect(outer, 10, 10)
        # inner inset shadow at top
        inset = outer.adjusted(0, 0, 0, -1)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(224, 178, 27, 80))
        painter.drawRoundedRect(inset, 10, 10)

        painter.setPen(QPen(QColor("#000000"), 3.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QColor("#111111"))

        if self.kind == "jewellery":
            self.draw_jewellery_icon(painter)
        elif self.kind == "scan":
            self.draw_scan_icon(painter)
        elif self.kind == "report":
            self.draw_report_icon(painter)
        elif self.kind == "history":
            self.draw_history_icon(painter)
        elif self.kind == "settings":
            self.draw_settings_icon(painter)

        if self.has_arrow:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#000000"))
            arrow = QPolygonF([
                QPointF(self.width() - 12, self.height() - 10),
                QPointF(self.width() - 6, self.height() - 10),
                QPointF(self.width() - 9, self.height() - 5)
            ])
            painter.drawPolygon(arrow)

    def draw_jewellery_icon(self, painter):
        # Diamond icon (replaces necklace)
        cx, cy = self.width() / 2.0, self.height() / 2.0

        top = QPointF(cx, cy - 20)
        left = QPointF(cx - 22, cy - 6)
        right = QPointF(cx + 22, cy - 6)
        bottom = QPointF(cx, cy + 26)

        # Outer diamond
        outer = QPolygonF([top, right, bottom, left])
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon(outer)

        # Upper facets
        mid_top = QPointF(cx, cy - 6)
        painter.drawLine(top, mid_top)
        painter.drawLine(left, mid_top)
        painter.drawLine(right, mid_top)

        # Lower facets
        painter.drawLine(mid_top, bottom)
        painter.drawLine(left, bottom)
        painter.drawLine(right, bottom)

        # Small sparkle (top-right)
        s = 6
        sx, sy = cx + 24, cy - 22
        painter.drawLine(QPointF(sx - s, sy), QPointF(sx + s, sy))
        painter.drawLine(QPointF(sx, sy - s), QPointF(sx, sy + s))

    def draw_scan_icon(self, painter):
        # Centered focus-frame + "A" like reference
        w, h = self.width(), self.height()
        cx, cy = w / 2.0, h / 2.0
        pad = 18
        left = cx - (w / 2.0 - pad)
        right = cx + (w / 2.0 - pad)
        top = cy - (h / 2.0 - pad)
        bottom = cy + (h / 2.0 - pad)

        # Corner brackets
        br_len = 16
        painter.drawLine(QPointF(left, top + br_len), QPointF(left, top))
        painter.drawLine(QPointF(left, top), QPointF(left + br_len, top))

        painter.drawLine(QPointF(right - br_len, top), QPointF(right, top))
        painter.drawLine(QPointF(right, top), QPointF(right, top + br_len))

        painter.drawLine(QPointF(left, bottom - br_len), QPointF(left, bottom))
        painter.drawLine(QPointF(left, bottom), QPointF(left + br_len, bottom))

        painter.drawLine(QPointF(right - br_len, bottom), QPointF(right, bottom))
        painter.drawLine(QPointF(right, bottom), QPointF(right, bottom - br_len))

        # Center letter
        font = QFont("Segoe UI", 24, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRectF(0, 0, self.width(), self.height()), Qt.AlignCenter, "M")

    def draw_report_icon(self, painter):
        # Centered report page with diamond
        w, h = self.width(), self.height()
        cx, cy = w / 2.0, h / 2.0

        page_w, page_h = w * 0.42, h * 0.52
        page_x = cx - page_w / 2.0
        page_y = cy - page_h / 2.0

        page = QPainterPath()
        page.addRect(page_x, page_y, page_w, page_h)
        painter.setBrush(QColor("#111111"))
        painter.drawPath(page)

        painter.setPen(QPen(QColor("#F7E09A"), 2))
        line_y1 = page_y + page_h * 0.20
        line_y2 = page_y + page_h * 0.30
        line_y3 = page_y + page_h * 0.40
        painter.drawLine(QPointF(page_x + 8, line_y1), QPointF(page_x + page_w * 0.65, line_y1))
        painter.drawLine(QPointF(page_x + 8, line_y2), QPointF(page_x + page_w * 0.72, line_y2))
        painter.drawLine(QPointF(page_x + 8, line_y3), QPointF(page_x + page_w * 0.55, line_y3))

        # Diamond icon centered in lower part
        dy_top = QPointF(cx, page_y + page_h * 0.55)
        dy_left = QPointF(cx - page_w * 0.18, page_y + page_h * 0.70)
        dy_right = QPointF(cx + page_w * 0.18, page_y + page_h * 0.70)
        dy_bottom = QPointF(cx, page_y + page_h * 0.88)
        diamond = QPolygonF([dy_top, dy_right, dy_bottom, dy_left])
        painter.drawPolygon(diamond)
        painter.drawLine(dy_top, dy_bottom)
        painter.drawLine(dy_left, dy_bottom)
        painter.drawLine(dy_right, dy_bottom)

    def draw_history_icon(self, painter):
        # Circular history arrow centered
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor("#111111"), 4.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        w, h = self.width(), self.height()
        cx, cy = w / 2.0, h / 2.0
        r = min(w, h) * 0.22
        rect = QRectF(cx - r, cy - r, 2 * r, 2 * r)

        painter.drawArc(rect, 40 * 16, 280 * 16)

        # Arrow head
        tip = QPointF(cx - r * 0.9, cy - r * 0.1)
        wing1 = QPointF(tip.x() - 6, tip.y() + 8)
        wing2 = QPointF(tip.x() + 2, tip.y() + 8)
        painter.drawLine(tip, wing1)
        painter.drawLine(tip, wing2)

        # Clock hands
        painter.drawLine(QPointF(cx, cy), QPointF(cx, cy - r * 0.6))
        painter.drawLine(QPointF(cx, cy), QPointF(cx + r * 0.6, cy))

    def draw_settings_icon(self, painter):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#111111"))

        w, h = self.width(), self.height()
        cx, cy = w / 2.0, h / 2.0
        r_outer, r_inner = min(w, h) * 0.28, min(w, h) * 0.20
        pts = []
        for i in range(16):
            angle = math.radians(i * 22.5)
            r = r_outer if i % 2 == 0 else r_inner
            pts.append(QPointF(cx + r * math.cos(angle), cy + r * math.sin(angle)))

        painter.drawPolygon(QPolygonF(pts))
        painter.setBrush(QColor("#F2DE8F"))
        painter.drawEllipse(QPointF(cx, cy), min(w, h) * 0.09, min(w, h) * 0.09)


class FocusSlider(QSlider):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(19)
        self.setFixedHeight(28)
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                background: white;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: black;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: white;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: black;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
        """)


class FocusPanel(QFrame):
    def __init__(self, gold_border="#DCC374", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #EFD989;
                border: 2px solid {gold_border};
                border-radius: 16px;
            }}
        """)
        self.setFixedHeight(180)
        self.setFixedWidth(470)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 22, 26, 20)
        layout.setSpacing(20)

        self.slider = FocusSlider()

        self.value_box = QLabel("19")
        self.value_box.setAlignment(Qt.AlignCenter)
        self.value_box.setFixedSize(160, 50)
        self.value_box.setStyleSheet("""
            QLabel {
                background: #F6F6F6;
                border: none;
                border-radius: 10px;
                color: #111111;
                font-family: Segoe UI;
                font-size: 22px;
                font-weight: 700;
            }
        """)

        value_wrap = QHBoxLayout()
        value_wrap.setContentsMargins(0, 0, 0, 0)
        value_wrap.addStretch()
        value_wrap.addWidget(self.value_box)
        value_wrap.addStretch()

        layout.addWidget(self.slider)
        layout.addLayout(value_wrap)

        self.slider.valueChanged.connect(self.update_value)

    def update_value(self, value):
        self.value_box.setText(f"{value:02d}")


class HomePage(QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("IDT Desktop Application")
        self.setStyleSheet("background-color: #F8F8F8;")
        self.resize_to_screen()
        self.setup_ui()

    def resize_to_screen(self):
        desktop = QDesktopWidget().availableGeometry()
        self.resize(desktop.width(), desktop.height())

    def open_compare_page(self):
        if self.stacked_widget is not None:
            self.stacked_widget.setCurrentIndex(4)

    def setup_ui(self):
        gold_border = "#DCC374"
        text_color = "#222222"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "..", "assets", "images", "logo.jpeg")
        logo_path = os.path.abspath(logo_path)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar
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
        left_header_layout = QHBoxLayout(left_widget)
        left_header_layout.setContentsMargins(0, 0, 0, 0)
        left_header_layout.setSpacing(10)

        logo_circle = ImageLabel(logo_path, 32, 32)

        brand_text = QLabel("SYD-PRO")
        brand_font = QFont("Segoe UI", 16)
        brand_font.setBold(True)
        brand_text.setFont(brand_font)
        brand_text.setStyleSheet(f"color: {text_color};")

        left_header_layout.addWidget(logo_circle)
        left_header_layout.addWidget(brand_text)
        left_header_layout.addStretch()

        title = QLabel("HOME")
        title_font = QFont("Segoe UI", 16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {text_color};")

        right_space = QWidget()

        top_layout.addWidget(left_widget, 1)
        top_layout.addWidget(title, 1)
        top_layout.addWidget(right_space, 1)

        # Center area
        center_frame = QFrame()
        center_frame.setStyleSheet("background-color: #F8F8F8;")
        center_layout = QHBoxLayout(center_frame)
        center_layout.setContentsMargins(6, 0, 6, 0)
        center_layout.setSpacing(0)

        # Left panel
        left_panel = QFrame()
        left_panel.setMinimumWidth(500)
        left_panel.setStyleSheet(f"""
            QFrame {{
                background-color: #F2F2F2;
                border: 1px solid {gold_border};
                border-right: none;
            }}
        """)
        left_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setContentsMargins(0, 0, 0, 0)
        left_panel_layout.setSpacing(0)

        preview_area = QWidget()
        preview_area.setStyleSheet("background-color: #F2F2F2;")
        preview_layout = QVBoxLayout(preview_area)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(8)
        preview_layout.setAlignment(Qt.AlignCenter)

        spinner = SpinnerWidget()
        preview_text = QLabel("Live Preview")
        preview_font = QFont("Segoe UI", 12)
        preview_text.setFont(preview_font)
        preview_text.setStyleSheet("color: #333333;")

        preview_layout.addWidget(spinner, alignment=Qt.AlignCenter)
        preview_layout.addWidget(preview_text, alignment=Qt.AlignCenter)

        left_panel_layout.addWidget(preview_area)

        # Right panel
        right_panel = QFrame()
        right_panel.setFixedWidth(570)
        right_panel.setStyleSheet(f"""
            QFrame {{
                background-color: #FAFAFA;
                border: 1px solid {gold_border};
            }}
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(18, 14, 18, 14)
        right_layout.setSpacing(8)

        # Logo row
        idt_logo_row = QHBoxLayout()
        idt_logo_row.setContentsMargins(0, 0, 0, 0)
        idt_logo_row.setSpacing(12)

        logo_top = QLabel("IDT")
        logo_top_font = QFont("Times New Roman", 36)
        logo_top.setFont(logo_top_font)
        logo_top.setAlignment(Qt.AlignVCenter)
        logo_top.setStyleSheet("color: #3C2B22; border: none;")

        company_logo = ImageLabel(logo_path, 70, 70)

        idt_logo_row.addStretch()
        idt_logo_row.addWidget(company_logo)
        idt_logo_row.addWidget(logo_top)
        idt_logo_row.addStretch()

        idt_logo_widget = QWidget()
        idt_logo_widget.setLayout(idt_logo_row)

        logo_sub = QLabel("IDT GEMOLOGICAL LABORATORIES WORLDWIDE")
        logo_sub_font = QFont("Segoe UI", 7)
        logo_sub.setFont(logo_sub_font)
        logo_sub.setAlignment(Qt.AlignCenter)
        logo_sub.setStyleSheet("color: #111111; border: none;")

        right_layout.addWidget(idt_logo_widget)
        right_layout.addWidget(logo_sub)

        # Form
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setContentsMargins(0, 6, 0, 0)
        form_layout.setHorizontalSpacing(14)
        form_layout.setVerticalSpacing(12)

        label_font = QFont("Segoe UI", 13)
        input_font = QFont("Segoe UI", 13)

        labels = ["Lot no:", "ID:", "Size:", "Remarks:"]
        self.inputs = []

        for row, txt in enumerate(labels):
            lab = QLabel(txt)
            lab.setFont(label_font)
            lab.setStyleSheet("color: #333333; border: none;")

            inp = QLineEdit()
            inp.setFont(input_font)
            inp.setFixedHeight(38)
            inp.setStyleSheet(f"""
                QLineEdit {{
                    background: #F8F8F8;
                    border: 1px solid {gold_border};
                    border-radius: 5px;
                    padding-left: 10px;
                    color: #222222;
                }}
            """)

            form_layout.addWidget(lab, row, 0)
            form_layout.addWidget(inp, row, 1)
            self.inputs.append(inp)

        right_layout.addWidget(form_widget)

        # gap after form
        right_layout.addSpacing(36)

        # Button row
        icon_row = QHBoxLayout()
        icon_row.setContentsMargins(24, 0, 24, 0)
        icon_row.setSpacing(10)

        self.btn_jewellery = SymbolButton("jewellery", has_arrow=True)
        self.btn_scan = SymbolButton("scan", has_arrow=True)
        self.btn_report = SymbolButton("report")
        self.btn_history = SymbolButton("history")
        self.btn_settings = SymbolButton("settings")

        self.btn_report.clicked.connect(self.open_compare_page)

        icon_row.addWidget(self.btn_jewellery)
        icon_row.addWidget(self.btn_scan)
        icon_row.addWidget(self.btn_report)
        icon_row.addWidget(self.btn_history)
        icon_row.addWidget(self.btn_settings)

        right_layout.addLayout(icon_row)

        # gap between icons and focus panel
        right_layout.addSpacing(24)

        # Focus panel centered
        focus_row = QHBoxLayout()
        focus_row.setContentsMargins(0, 0, 0, 0)
        focus_row.addStretch()
        self.focus_panel = FocusPanel(gold_border)
        focus_row.addWidget(self.focus_panel)
        focus_row.addStretch()

        right_layout.addLayout(focus_row)

        right_layout.addStretch()

        # Bottom buttons centered
        bottom_btn_row = QHBoxLayout()
        bottom_btn_row.setContentsMargins(8, 2, 8, 8)
        bottom_btn_row.setSpacing(22)

        scan_btn = QPushButton("SCAN")
        scan_btn.setFixedSize(160, 56)
        scan_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #F8F8F8;
                border: 1px solid {gold_border};
                border-radius: 7px;
                color: #111111;
                font-family: Segoe UI;
                font-size: 18px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #FCFCFC;
            }}
        """)

        adv_btn = QPushButton("Advance Analysis")
        adv_btn.setFixedSize(250, 56)
        adv_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #F8F8F8;
                border: 1px solid {gold_border};
                border-radius: 7px;
                color: #111111;
                font-family: Segoe UI;
                font-size: 17px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #FCFCFC;
            }}
        """)

        bottom_btn_row.addStretch()
        bottom_btn_row.addWidget(scan_btn)
        bottom_btn_row.addWidget(adv_btn)
        bottom_btn_row.addStretch()

        right_layout.addLayout(bottom_btn_row)

        center_layout.addWidget(left_panel, 1)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = HomePage()
    window.showMaximized()

    sys.exit(app.exec_())