from io import BytesIO
import sys

import qrcode
from PIL import Image
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QGroupBox,
)

class QRGeneratorWidget(QGroupBox):
    def __init__(self, title="QR 코드"):
        super().__init__(title)
        self.qr_image = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("URL 또는 텍스트를 입력하세요")

        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("생성")
        self.generate_btn.clicked.connect(self.on_generate)

        self.save_btn = QPushButton("저장")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.on_save)

        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.save_btn)

        self.preview = QLabel()
        self.preview.setFixedSize(200, 200)
        self.preview.setStyleSheet("border: 1px solid #ccc; background-color: #f9f9f9;")
        self.preview.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.input)
        layout.addLayout(btn_layout)
        layout.addWidget(self.preview)

        self.setLayout(layout)

    def on_generate(self):
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "입력 필요", "URL 또는 텍스트를 입력하세요.")
            return

        try:
            img = self.generate_qr_image(text)
            self.qr_image = img
            pix = self.pil_image_to_qpixmap(img)
            self.preview.setPixmap(pix.scaled(self.preview.width(), self.preview.height(), Qt.KeepAspectRatio))
            self.save_btn.setEnabled(True)
        except ValueError as e:
            QMessageBox.critical(self, "생성 오류", str(e))

    def on_save(self):
        if self.qr_image is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "이미지 저장", "qrcode.png", "PNG Files (*.png)")
        if path:
            try:
                self.qr_image.save(path, format="PNG")
            except Exception as e:
                QMessageBox.critical(self, "저장 오류", f"이미지를 저장하지 못했습니다:\n{e}")

    @staticmethod
    def generate_qr_image(data: str, box_size: int = 10, border: int = 4) -> Image.Image:
        # 데이터가 너무 길 때 발생하는 에러를 방지하기 위해 최적화된 설정 사용
        qr = qrcode.QRCode(
            version=None,  # 자동 조절
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # 데이터 수용량 극대화
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        
        try:
            qr.make(fit=True)
        except ValueError:
            raise ValueError("입력한 데이터가 QR 코드의 최대 용량을 초과했습니다.")
            
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        return img

    @staticmethod
    def pil_image_to_qpixmap(img: Image.Image) -> QPixmap:
        buf = BytesIO()
        img.save(buf, format="PNG")
        qimg = QImage.fromData(buf.getvalue())
        return QPixmap.fromImage(qimg)


class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR 코드 생성기 (Multi)")
        self.resize(380, 700)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        # 4개의 QR 생성 위젯 추가
        for i in range(4):
            qr_widget = QRGeneratorWidget(f"QR 코드 {i+1} 세트")
            scroll_layout.addWidget(qr_widget)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    win = QRCodeGenerator()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()