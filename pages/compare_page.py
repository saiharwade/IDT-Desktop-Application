import os
from PyQt5.QtCore import Qt, QPointF, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QPixmap, QPolygonF
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QFrame
from PyQt5.QtCore import pyqtSignal


class ImageLabel(QLabel):
    def __init__(self, image_path="", parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: none; background: transparent;")
        self._image_path = image_path

    def refresh(self):
        self.clear()
        if self._image_path and os.path.exists(self._image_path):
            pixmap = QPixmap(self._image_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.setPixmap(scaled)
                return
        self.setText("◎")
        self.setStyleSheet(
            "background-color:#E7C75D;border:1px solid #CFAE47;border-radius:17px;color:#111111;"
        )


class StripeBar(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, filled=7, total=18, parent=None):
        super().__init__(parent)
        self.filled = int(filled)
        self.total = total
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

    def value(self) -> int:
        return int(self.filled)

    def setValue(self, v: int):
        v = int(v)
        v = max(0, min(v, int(self.total)))
        if v != int(self.filled):
            self.filled = v
            self.valueChanged.emit(v)
            self.update()

    def _value_from_pos(self, x: int) -> int:
        w = max(1, self.width())
        x = max(0, min(int(x), w - 1))

        gap = max(1, int(w * 0.012))
        seg_w = max(6, int((w - (int(self.total) - 1) * gap) / int(self.total)))
        pitch = seg_w + gap

        idx = int(x / pitch)
        idx = max(0, min(idx, int(self.total) - 1))
        # value is "filled segments count"
        return idx + 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w = max(1, self.width())
        h = max(1, self.height())

        # Reference-style tapered segmented bar
        outline = QColor("#EDC84A")
        filled_col = QColor("#D9B63A")
        empty_col = QColor("#F7F7F7")
        empty_outline = QColor("#BFC3C7")
        marker_col = QColor("#6F6F6F")

        gap = max(1, int(w * 0.012))
        seg_w = max(6, int((w - (self.total - 1) * gap) / self.total))
        y_top = max(1, int(h * 0.14))
        y_bot = max(y_top + 6, int(h * 0.86))

        # Taper: left segments are thinner, gradually increase to full height
        min_thickness = max(6, int(h * 0.22))
        max_thickness = max(10, int(h * 0.72))

        for i in range(self.total):
            x0 = i * (seg_w + gap)
            x1 = x0 + seg_w

            t0 = i / max(1, (self.total - 1))
            t1 = (i + 1) / max(1, (self.total - 1))
            th0 = min_thickness + (max_thickness - min_thickness) * t0
            th1 = min_thickness + (max_thickness - min_thickness) * t1

            # Build a trapezoid segment (top edge rises with taper)
            seg = QPolygonF(
                [
                    QPointF(x0, y_bot),
                    QPointF(x1, y_bot),
                    QPointF(x1, y_bot - th1),
                    QPointF(x0, y_bot - th0),
                ]
            )

            if i < self.filled:
                painter.setBrush(filled_col)
                painter.setPen(QPen(outline, 1))
            else:
                painter.setBrush(empty_col)
                painter.setPen(QPen(empty_outline, 1))

            painter.drawPolygon(seg)

        # Center marker line (like reference)
        marker_x = int(w * 0.50)
        painter.setPen(QPen(marker_col, max(2, int(w * 0.01))))
        painter.drawLine(marker_x, y_top, marker_x, y_bot)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setValue(self._value_from_pos(event.x()))
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.setValue(self._value_from_pos(event.x()))
            event.accept()
            return
        super().mouseMoveEvent(event)


class ComparePage(QWidget):
    BASE_W = 1920
    BASE_H = 1200

    def __init__(self, stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setStyleSheet("background-color: #FFFFFF;")
        self._geo = []
        self._fonts = []
        self._logo_widgets = []
        self._line_edits = []
        self._advanced_open = False
        self._advanced_widgets = []
        self._build_ui()
        self._set_advanced_open(False)
        self._apply_scaled_layout()

    def go_home(self):
        if self.stacked_widget is not None:
            self.stacked_widget.setCurrentIndex(1)

    def _set_advanced_open(self, is_open: bool):
        self._advanced_open = bool(is_open)
        for w in self._advanced_widgets:
            w.setVisible(self._advanced_open)

    def _toggle_advanced(self):
        self._set_advanced_open(not self._advanced_open)

    def _add_geo(self, widget, x, y, w, h):
        self._geo.append((widget, QRect(x, y, w, h)))
        return widget

    def _add_font(self, widget, family, px, weight=QFont.Normal, italic=False):
        self._fonts.append((widget, family, px, weight, italic))
        return widget

    def _button_style(self):
        return """
            QPushButton {
                background-color: #F8F8F8;
                border: 1px solid #EDC84A;
                border-radius: 9px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #FCFCFC;
            }
        """

    def _line_edit_style(self):
        return """
            QLineEdit {
                background-color: #F8F8F8;
                border: 1px solid #EDC84A;
                border-radius: 10px;
                color: #000000;
                padding-left: 10px;
            }
        """

    def _build_ui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.abspath(os.path.join(current_dir, "..", "assets", "images", "logo.jpeg"))

        self.canvas = QWidget(self)
        self.canvas.setStyleSheet("background-color: #FFFFFF;")
        self._add_geo(self.canvas, 0, 0, self.BASE_W, self.BASE_H)

        top_bar = self._add_geo(QFrame(self.canvas), 0, 0, 1920, 111)
        top_bar.setStyleSheet("background-color:#F8F8F8;border-bottom:1px solid #EDC84A;")

        left_bg = self._add_geo(QFrame(self.canvas), 0, 112, 1362, 1009)
        left_bg.setStyleSheet("background-color:#F3F3F3;border:none;")

        right_bg = self._add_geo(QFrame(self.canvas), 1362, 112, 558, 1009)
        right_bg.setStyleSheet("background-color:#FAFAFA;border-left:1px solid #EDC84A;")

        footer = self._add_geo(QFrame(self.canvas), 0, 1121, 1920, 79)
        footer.setStyleSheet("background-color:#F8F8F8;border-top:1px solid #EDC84A;")

        # Left four result regions with Figma split lines.
        for x, y, w, h in [(0, 112, 682, 499), (682, 112, 680, 499), (0, 611, 682, 510), (682, 611, 680, 510)]:
            box = self._add_geo(QFrame(self.canvas), x, y, w, h)
            box.setStyleSheet("background-color:#F3F3F3;border:1px solid #EDC84A;")

        small_labels = [
            ("Result", 21, 124),
            ("Flourescense", 702, 124),
            ("Short Phosphorous", 21, 623),
            ("Long Phosphorous", 702, 620),
        ]
        for text, x, y in small_labels:
            lbl = self._add_geo(QLabel(text, self.canvas), x, y, 320, 32)
            lbl.setStyleSheet("color: rgba(0,0,0,0.6); background: transparent;")
            self._add_font(lbl, "Poppins", 27, QFont.Light)

        logo_small = self._add_geo(ImageLabel(logo_path, self.canvas), 20, 14, 72, 72)
        self._logo_widgets.append(logo_small)

        brand = self._add_geo(QLabel("SYD-PRO", self.canvas), 141, 22, 220, 56)
        brand.setStyleSheet("color:#000000;background:transparent;")
        self._add_font(brand, "Inter", 44, QFont.Normal)

        title = self._add_geo(QLabel("COMPARE", self.canvas), 895, 28, 240, 52)
        title.setStyleSheet("color:#000000;background:transparent;")
        self._add_font(title, "Poppins", 39, QFont.Bold)

        footer_left = self._add_geo(QLabel("IDT Gemological Laborateries Worldwide", self.canvas), 68, 1143, 740, 49)
        footer_left.setStyleSheet("color:#000000;background:transparent;")
        self._add_font(footer_left, "Poppins", 30, QFont.Medium)

        footer_right = self._add_geo(QLabel("www.idtworldwide.com", self.canvas), 1476, 1136, 390, 48)
        footer_right.setStyleSheet("color:#000000;background:transparent;")
        self._add_font(footer_right, "Poppins", 32, QFont.Medium)

        # Right panel brand (centered block: logo + IDT centered as a group).
        right_panel_x = 1362
        right_panel_w = 558
        right_center_x = right_panel_x + right_panel_w // 2  # 1641 in base coords

        brand_block_y = 140
        logo_w = 92
        logo_h = 92
        gap = 18
        idt_w = 260
        idt_h = 96
        group_w = logo_w + gap + idt_w
        group_left_x = right_center_x - group_w // 2

        rp_logo = self._add_geo(ImageLabel(logo_path, self.canvas), group_left_x, brand_block_y, logo_w, logo_h)
        self._logo_widgets.append(rp_logo)

        rp_idt = self._add_geo(
            QLabel("IDT", self.canvas),
            group_left_x + logo_w + gap,
            brand_block_y - 2,
            idt_w,
            idt_h,
        )
        rp_idt.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        rp_idt.setStyleSheet("color:#2B2B2B;background:transparent;")
        # Closer to reference: larger, elegant serif
        self._add_font(rp_idt, "Times New Roman", 74, QFont.Normal)

        rp_sub = self._add_geo(
            QLabel("IDT GEMOLOGICAL LABORATORIES WORLDWIDE", self.canvas),
            right_panel_x,
            brand_block_y + logo_h + 6,
            right_panel_w,
            30,
        )
        rp_sub.setStyleSheet("color:#000000;background:transparent;")
        rp_sub.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self._add_font(rp_sub, "Poppins", 15, QFont.Medium)

        # Inputs and labels.
        hpht = self._add_geo(QLabel("HPHT:", self.canvas), 1387, 297, 100, 40)
        cvd = self._add_geo(QLabel("CVD:", self.canvas), 1386, 366, 100, 40)
        for lbl in [hpht, cvd]:
            lbl.setStyleSheet("color:#000000;background:transparent;")
            self._add_font(lbl, "Poppins", 27, QFont.Light)

        self.hpht_input = self._add_geo(QLineEdit(self.canvas), 1518, 299, 331, 40)
        self.cvd_input = self._add_geo(QLineEdit(self.canvas), 1518, 366, 331, 40)
        for le in [self.hpht_input, self.cvd_input]:
            le.setStyleSheet(self._line_edit_style())
            self._add_font(le, "Poppins", 20, QFont.Normal)
            self._line_edits.append(le)

        # Step controls.
        self.plus_btn = self._add_geo(QPushButton("+", self.canvas), 1566, 436, 61, 40)
        self.value_lbl = self._add_geo(QLabel("00", self.canvas), 1638, 436, 91, 40)
        self.minus_btn = self._add_geo(QPushButton("-", self.canvas), 1740, 436, 61, 40)
        for b in [self.plus_btn, self.minus_btn]:
            b.setStyleSheet(self._button_style())
            self._add_font(b, "Poppins", 27, QFont.Light)
        self.value_lbl.setAlignment(Qt.AlignCenter)
        self.value_lbl.setStyleSheet("background-color:#F8F8F8;border:1px solid #EDC84A;border-radius:10px;color:#000000;")
        self._add_font(self.value_lbl, "Poppins", 27, QFont.Light)

        # Action buttons.
        self.high_gain_btn = self._add_geo(QPushButton("High gain", self.canvas), 1389, 526, 203, 40)
        self.simulant_btn = self._add_geo(QPushButton("Simulant", self.canvas), 1646, 526, 203, 40)
        self.advance_btn = self._add_geo(QPushButton("Advance Analysis", self.canvas), 1497, 599, 262, 40)
        for b in [self.high_gain_btn, self.simulant_btn, self.advance_btn]:
            b.setStyleSheet(self._button_style())
            self._add_font(b, "Poppins", 27, QFont.Light)
        self.advance_btn.clicked.connect(self._toggle_advanced)

        # Meter labels and bars.
        meter_labels = [("Gain:", 1388, 677), ("Exposer:", 1387, 735), ("Shutter:", 1387, 791), ("ISO:", 1386, 851)]
        fills = [7, 6, 5, 5]
        self.meter_bars = []
        for (txt, x, y), f in zip(meter_labels, fills):
            lbl = self._add_geo(QLabel(txt, self.canvas), x, y, 130, 32)
            lbl.setStyleSheet("color:#000000;background:transparent;")
            self._add_font(lbl, "Poppins", 27, QFont.Light)
            bar = self._add_geo(StripeBar(f, 18, self.canvas), 1518, y, 331, 28)
            self.meter_bars.append(bar)
            self._advanced_widgets.extend([lbl, bar])

        # Bottom navigation.
        self.home_btn = self._add_geo(QPushButton("Home", self.canvas), 1393, 995, 106, 52)
        self.result_btn = self._add_geo(QPushButton("Result", self.canvas), 1541, 995, 94, 52)
        self.cert_btn = self._add_geo(QPushButton("Certificate", self.canvas), 1678, 995, 171, 52)
        for b in [self.home_btn, self.result_btn, self.cert_btn]:
            b.setStyleSheet(self._button_style())
            self._add_font(b, "Poppins", 21, QFont.Medium)

        self.home_btn.clicked.connect(self.go_home)

    def _apply_scaled_layout(self):
        sx = self.width() / float(self.BASE_W) if self.BASE_W else 1.0
        sy = self.height() / float(self.BASE_H) if self.BASE_H else 1.0
        sf = min(sx, sy)

        for widget, rect in self._geo:
            widget.setGeometry(
                int(rect.x() * sx),
                int(rect.y() * sy),
                max(1, int(rect.width() * sx)),
                max(1, int(rect.height() * sy)),
            )

        for widget, family, px, weight, italic in self._fonts:
            font = QFont(family)
            font.setWeight(weight)
            font.setItalic(italic)
            font.setPixelSize(max(8, int(px * sf)))
            widget.setFont(font)

        radius = max(4, int(10 * sf))
        for le in self._line_edits:
            le.setStyleSheet(
                f"QLineEdit{{background-color:#F8F8F8;border:1px solid #EDC84A;border-radius:{radius}px;color:#000000;padding-left:{max(6, int(10*sf))}px;}}"
            )

        for logo in self._logo_widgets:
            logo.refresh()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_scaled_layout()