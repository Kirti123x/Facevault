import os

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from core.database import Database


class PersonGallery(QWidget):

    def __init__(self, person_name):
        super().__init__()

        self.person_name = person_name
        self.database = Database()

        self.setWindowTitle(f"{person_name}'s Photos")
        self.resize(900, 700)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel(f"{self.person_name}'s Photos")

        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.grid = QGridLayout()
        self.grid.setSpacing(15)

        layout.addLayout(self.grid)

        self.load_photos()

    def clear_grid(self):
        while self.grid.count():

            item = self.grid.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()



    def load_photos(self):
        self.clear_grid()

        person = self.database.get_person_by_name(
            self.person_name
        )

        if person is None:
            return

        person_id = person[0]

        photos = self.database.get_person_photos(
            person_id
        )

        row = 0
        col = 0

        shown = set()

        for photo in photos:

            image_path = photo[0]

            # Avoid showing the same photo multiple times
            if image_path in shown:
                continue

            shown.add(image_path)

            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                continue

            label = QLabel()

            label.setPixmap(
                pixmap.scaled(
                    220,
                    220,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            label.setFixedSize(
                230,
                230
            )

            self.grid.addWidget(
                label,
                row,
                col
            )

            col += 1

            if col >= 4:
                col = 0
                row += 1