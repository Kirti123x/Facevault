from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)

from core.indexer import FaceIndexer


class IndexWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(
        self,
        folder
    ):

        super().__init__()
        self.folder = folder

    def update_progress(
        self,
        value
    ):

        self.progress.emit(
            value
        )

    def run(self):
        indexer = FaceIndexer()
        indexer.index_folder(
            self.folder,
            self.update_progress
        )
        self.finished.emit()