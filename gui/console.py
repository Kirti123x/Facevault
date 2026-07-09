import sys
import datetime

from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QObject, pyqtSignal


class StreamRedirector(QObject):
    """
    File-like object that can replace sys.stdout / sys.stderr.

    Text written to it (from print(), exceptions, worker threads, etc.)
    is emitted as a Qt signal so it can be safely appended to a widget
    living on the main GUI thread, no matter which thread wrote it.
    """

    message_written = pyqtSignal(str)

    def write(self, text):
        if text:
            self.message_written.emit(str(text))

    def flush(self):
        # Required for file-like interface; nothing to flush.
        pass


class ConsoleWidget(QTextEdit):
    """
    A read-only, terminal-styled text box that shows everything
    printed by the application (stdout and stderr).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setMinimumHeight(160)

        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 12px;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 6px;
            }
        """)

        self._buffer = ""

    def append_text(self, text):
        # Buffer partial lines coming from print()'s separate
        # calls (text, then "\n") so we don't spam empty lines.
        self._buffer += text

        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            self._write_line(line)

    def _write_line(self, line):
        if line.strip() == "":
            return

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        self.append(f"[{timestamp}] {line}")

        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def attach_to_streams(self):
        """
        Redirects sys.stdout and sys.stderr into this console widget.
        Returns the redirector objects so callers can keep a reference
        (and restore the original streams later if desired).
        """

        stdout_redirector = StreamRedirector()
        stderr_redirector = StreamRedirector()

        stdout_redirector.message_written.connect(self.append_text)
        stderr_redirector.message_written.connect(self.append_text)

        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

        return stdout_redirector, stderr_redirector
