from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QProgressBar,
    QFrame,
    QMessageBox
)

from PyQt6.QtCore import Qt
from gui.gallery import GalleryPage
from gui.console import ConsoleWidget


class HomeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.folder_path = None
        self.gallery_window = None

        self.setWindowTitle("FaceVault")
        self.setGeometry(200, 100, 1200, 700)

        self.init_ui()

        # Redirect all print()/stdout/stderr output from anywhere in the
        # app (including background indexing threads) into the console box.
        self._stdout_redirector, self._stderr_redirector = (
            self.console.attach_to_streams()
        )

        print("FaceVault started. Ready.")

    def init_ui(self):

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)

        # =====================
        # Sidebar
        # =====================

        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)

        logo = QLabel("FaceVault")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        self.home_btn = QPushButton("Home")

        self.gallery_btn = QPushButton("People Gallery")
        self.gallery_btn.clicked.connect(self.open_gallery)

        self.settings_btn = QPushButton("Settings")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.home_btn)
        sidebar_layout.addWidget(self.gallery_btn)
        sidebar_layout.addWidget(self.settings_btn)
        sidebar_layout.addStretch()

        # =====================
        # Main Content
        # =====================

        content = QWidget()
        content_layout = QVBoxLayout(content)

        title = QLabel("AI Photo Organizer")
        title.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
        """)

        subtitle = QLabel(
            "Find and group photos automatically using AI face recognition."
        )

        self.select_btn = QPushButton("Select Image Folder")
        self.select_btn.clicked.connect(self.select_folder)

        self.folder_label = QLabel("No folder selected")

        self.index_btn = QPushButton("Start Indexing")
        self.index_btn.clicked.connect(self.start_indexing)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.status = QLabel("Ready")

        console_label = QLabel("Console Output")
        console_label.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        self.console = ConsoleWidget()

        content_layout.addWidget(title)
        content_layout.addWidget(subtitle)
        content_layout.addSpacing(30)
        content_layout.addWidget(self.select_btn)
        content_layout.addWidget(self.folder_label)
        content_layout.addSpacing(20)
        content_layout.addWidget(self.index_btn)
        content_layout.addWidget(self.progress)
        content_layout.addWidget(self.status)
        content_layout.addSpacing(20)
        content_layout.addWidget(console_label)
        content_layout.addWidget(self.console, stretch=1)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

    # =====================
    # Folder Selection
    # =====================

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Image Folder"
        )

        if folder:
            self.folder_path = folder
            self.folder_label.setText(folder)
            self.status.setText("Folder selected")
            print(f"Selected folder: {folder}")

    # =====================
    # Start Indexing
    # =====================

    def start_indexing(self):

        if not self.folder_path:

            QMessageBox.warning(
                self,
                "No Folder Selected",
                "Please select an image folder first."
            )
            return

        self.progress.setValue(0)
        self.status.setText("Indexing images...")

        self.index_btn.setEnabled(False)

        print(f"Starting indexing for folder: {self.folder_path}")

        from gui.Faceindexer import IndexWorker

        self.worker = IndexWorker(self.folder_path)

        self.worker.progress.connect(self.progress.setValue)

        self.worker.finished.connect(
            self.indexing_finished
        )

        self.worker.start()

    # =====================
    # Finished
    # =====================

    def indexing_finished(self):

        self.progress.setValue(100)

        self.status.setText(
            "Indexing completed successfully."
        )

        self.index_btn.setEnabled(True)

        print("Indexing finished successfully.")

        if self.gallery_window:

            try:
                self.gallery_window.load_people()
            except Exception:
                pass

        QMessageBox.information(
            self,
            "Completed",
            "Face indexing finished successfully."
        )

    # =====================
    # Gallery
    # =====================

    def open_gallery(self):

        if self.gallery_window is None:

            self.gallery_window = GalleryPage()

        self.gallery_window.show()
        self.gallery_window.raise_()
        self.gallery_window.activateWindow()