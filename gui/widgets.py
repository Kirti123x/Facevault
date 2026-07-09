from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal
)

from PyQt6.QtGui import QPixmap


class PersonCard(QFrame):

    clicked = pyqtSignal(str)

    def __init__(self, name, image_path=None):

        super().__init__()

        self.name = name

        self.setFixedSize(180,220)

        self.setStyleSheet("""
            QFrame{
                border:1px solid #cccccc;
                border-radius:10px;
            }
        """)

        layout = QVBoxLayout(self)

        self.image = QLabel()

        self.image.setFixedSize(140,140)

        self.image.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        if image_path:

            pixmap = QPixmap(image_path)

            if not pixmap.isNull():

                self.image.setPixmap(

                    pixmap.scaled(
                        140,
                        140,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )

            else:

                self.image.setText("👤")

        else:

            self.image.setText("👤")
            self.image.setStyleSheet("font-size:60px;")

        label = QLabel(name)

        label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.image)

        layout.addWidget(label)

    def mousePressEvent(self,event):

        self.clicked.emit(self.name)