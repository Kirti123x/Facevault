import sys
import traceback
from PyQt6.QtWidgets import QApplication

from gui.home import HomeWindow


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("FaceVault")

    window = HomeWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        input("Press Enter to exit...")