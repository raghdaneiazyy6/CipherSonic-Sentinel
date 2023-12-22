import sys
from os import path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QCoreApplication
from recorder import record_audio

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "design.ui"))

class CipherSonicApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(CipherSonicApp, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("CipherSonic Sentinel")

        # Connect the mousePressEvent to record_voice method
        self.recorderLabel.mousePressEvent = self.record_voice

        # Load image icons as QPixmap variables
        self.load_icons()

        # Set window icon
        self.setWindowIcon(QtGui.QIcon("media/appIcon.png"))

        # Set initial pixmaps
        self.set_initial_pixmaps()

    def load_icons(self):
        self.microphoneIcon = self.load_and_scale_icon("media/micIcon.png", self.recorderLabel.width())
        self.recordingIcon = self.load_and_scale_icon("media/recordingIcon.png", self.recorderLabel.width())
        self.lockedIcon = self.load_and_scale_icon("media/lockedIcon.png", self.lockLabel.width())
        self.unlockedIcon = self.load_and_scale_icon("media/unlockedIcon.png", self.lockLabel.width())

        # Store the original scaled pixmap
        self.originalMicrophoneIcon = self.microphoneIcon
        self.originalRecordingIcon = self.recordingIcon
        self.originalLockedIcon = self.lockedIcon
        self.originalUnlockedIcon = self.unlockedIcon

    def load_and_scale_icon(self, filename, width):
        return QPixmap(filename).scaledToWidth(width, Qt.SmoothTransformation)

    def set_initial_pixmaps(self):
        self.recorderLabel.setPixmap(self.originalMicrophoneIcon)
        self.lockLabel.setPixmap(self.unlockedIcon)

    def record_voice(self, event):
        filename = "recording.wav"

        self.recorderLabel.setPixmap(self.originalRecordingIcon)
        QCoreApplication.processEvents()

        # Record audio during the timeout interval
        record_audio()

        self.recorderLabel.setPixmap(self.originalMicrophoneIcon)
        print(f"Voice recorded and saved as '{filename}'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CipherSonicApp()
    window.show()
    sys.exit(app.exec_())
