from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout
)

from gui.widgets import PersonCard
from core.database import Database
from gui.person_gallery import PersonGallery


class GalleryPage(QWidget):

    def __init__(self):
        super().__init__()

        self.database = Database()

        self.setWindowTitle("People Gallery")
        self.resize(1000, 700)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Detected People")
        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        layout.addLayout(self.grid)

        self.load_people()

    def clear_grid(self):

        while self.grid.count():

            item = self.grid.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def load_people(self):

        self.clear_grid()

        people = self.database.get_people()

        row = 0
        col = 0

        for person in people:

            person_id = person[0]
            name = person[1]

            # Get person's photos
            photos = self.database.get_person_photos(person_id)

            thumbnail = None

            if len(photos) > 0:
                thumbnail = photos[0][1]

            card = PersonCard(
                name,
                thumbnail
            )

            card.clicked.connect(self.open_person)

            self.grid.addWidget(
                card,
                row,
                col
            )

            col += 1

            if col >= 4:
                col = 0
                row += 1

    def open_person(self, name):

        self.person_window = PersonGallery(name)
        self.person_window.show()

    def refresh(self):
        self.load_people()