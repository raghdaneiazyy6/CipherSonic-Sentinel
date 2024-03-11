from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUiType
from os import path
import sounddevice as sd
import librosa
import numpy as np
from model import load_model, extract_features
import wavio as wv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "design.ui"))

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        FigureCanvasQTAgg.updateGeometry(self)

class CipherSonicApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(CipherSonicApp, self).__init__(parent)
        QMainWindow.__init__(self, parent=None)
        self.setupUi(self)
        self.setWindowTitle("CipherSonic Sentinel")
        self.setWindowIcon(QtGui.QIcon("media/appIcon.png"))

        self.load_icons()
        self.set_initial_pixmaps()
        self.recorderLabel.setPixmap(self.microphoneIcon)
        self.lockLabel.setPixmap(self.lockedIcon)

        self.model_sentence, self.model_speaker = load_model()
        self.recorderLabel.mousePressEvent = self.record_voice
        self.anyoneCheckbox.stateChanged.connect(self.handleSelectedIndividuals)

        self.canvas = MplCanvas(self.spectrogramWidget)
        self.verticalLayout.addWidget(self.canvas)

        # {'Give me access': 0, 'Open the door': 1, 'Unlock middle gate': 2}
        # {'Ahmed': 0, 'Hazem': 2, 'Nourhan': 5, 'Raghda': 6, 'Samer': 7, 'Ali': 1, 'Mariem': 3, 'Nariman': 4}

    def handleSelectedIndividuals(self):
        if(self.anyoneCheckbox.isChecked()):
            self.listWidget.setEnabled(False)
        else:
            self.listWidget.setEnabled(True)

    def locked(self):
        self.lockWordLabel.setText("Locked")
        self.lockWordLabel.setStyleSheet("color: rgb(223, 0, 0); background-color: rgb(190, 190, 190);")
        self.accessLabel.setText("Nice try, but the vocal cords say 'access denied'.")
        self.accessLabel.setStyleSheet("color: rgb(223, 0, 0); background-color: rgb(190, 190, 190);")
        self.lockLabel.setPixmap(self.lockedIcon)

    def load_icons(self):
        self.microphoneIcon = self.load_and_scale_icon("media/micIcon.png", self.recorderLabel.width())
        self.recordingIcon = self.load_and_scale_icon("media/recordingIcon.png", self.recorderLabel.width())
        self.lockedIcon = self.load_and_scale_icon("media/lockedIcon.png", self.lockLabel.width())
        self.unlockedIcon = self.load_and_scale_icon("media/unlockedIcon.png", self.lockLabel.width())

    def load_and_scale_icon(self, filename, width):
        return QPixmap(filename).scaledToWidth(width, Qt.SmoothTransformation)

    def set_initial_pixmaps(self):
        self.recorderLabel.setPixmap(self.microphoneIcon)
        self.lockLabel.setPixmap(self.lockedIcon)

    def record_audio(self, duration, filename="recording.wav"):
            self.recorderLabel.setPixmap(self.recordingIcon)
            self.recorderLabel.repaint()
            fs = 44100
            recording = sd.rec(duration * fs, samplerate=fs, channels=1)
            sd.wait()
            wv.write(filename, recording, fs, sampwidth=2)

    def record_voice(self, event):
        filename = "recording.wav"
        self.record_audio(duration=2)
        self.recorderLabel.setPixmap(self.microphoneIcon)
        self.plot_spectrogram(filename)
        sentence_probabilites, speaker_probabilites = self.predict()
        self.analyze(sentence_probabilites, speaker_probabilites)
        self.draw_tables(sentence_probabilites, speaker_probabilites)
    
    def draw_tables(self, sentence_probabilites, speaker_probabilites):

        # To get the array inside the array
        matching_percentages_sentence = sentence_probabilites[0]
        matching_percentages_speaker = speaker_probabilites[0]

        sentence_table = QtGui.QStandardItemModel()
        sentence_table.setHorizontalHeaderItem(0, QtGui.QStandardItem("Passcode"))
        sentence_table.setHorizontalHeaderItem(1, QtGui.QStandardItem("Sentence Matching %"))

        sentences = ["Give me access", "Open the door", "Other sentence", "Unlock middle gate"]

        for sentence_label, matching_percentage in zip(sentences, matching_percentages_sentence):
            item_sentence = QtGui.QStandardItem(sentence_label)
            item_matching_percentage = QtGui.QStandardItem(f"{matching_percentage * 100:.2f}%")

            sentence_table.appendRow([item_sentence, item_matching_percentage])

        speaker_table = QtGui.QStandardItemModel()
        speaker_table.setHorizontalHeaderItem(0, QtGui.QStandardItem("Speaker"))
        speaker_table.setHorizontalHeaderItem(1, QtGui.QStandardItem("Speaker Matching %"))

        speakers = ["Ahmed", "Ali", "Hazem", "Mariem", "Nariman", "Nourhan", "Raghda", "Samer"]

        for speaker_label, matching_percentage in zip(speakers, matching_percentages_speaker):
            item_speaker = QtGui.QStandardItem(speaker_label)
            item_matching_percentage_speaker = QtGui.QStandardItem(f"{matching_percentage * 100:.2f}%")
            speaker_table.appendRow([item_speaker, item_matching_percentage_speaker])

        self.resultsTable1.setModel(sentence_table)
        self.resultsTable1.resizeRowsToContents()
        self.resultsTable2.setModel(speaker_table)

    def compute_spectrogram(self, audio_path):
        y, sr = librosa.load(audio_path)
        spectrogram = np.abs(librosa.stft(y))
        return spectrogram

    def plot_spectrogram(self, filename):
        spec_instant = self.compute_spectrogram(filename)
        if not hasattr(self, 'image'):
            self.image = self.canvas.axes.imshow(np.log1p(spec_instant), aspect='auto', origin='lower', cmap='viridis')
            self.colorbar = self.canvas.fig.colorbar(self.image, ax=self.canvas.axes, orientation='vertical')
        else:
            self.image.set_array(np.log1p(spec_instant))
            self.image.autoscale()
        self.canvas.draw()

    def unlocked(self):
        self.lockWordLabel.setText("Unlocked")
        self.lockWordLabel.setStyleSheet("color: rgb(18, 134, 61); background-color: rgb(190, 190, 190);")
        self.accessLabel.setText("Voiceprint confirmed: Your vocal cords undoubtedly silenced denial.")
        self.accessLabel.setStyleSheet("color: rgb(18, 134, 61); background-color: rgb(190, 190, 190);")
        self.lockLabel.setPixmap(self.unlockedIcon)

    def analyze(self, sentence_probabilites, speaker_probabilites):
        selected_items = self.listWidget.selectedItems()
        selected_indices = [self.listWidget.row(item) for item in selected_items]
        selected_indices.sort()

        if(self.anyoneCheckbox.isChecked()): # Mode 1
            if(np.argmax(sentence_probabilites) in [0, 1, 3]):
                self.unlocked()
            else:
                self.locked()
        else: # Mode 2
            if (np.argmax(speaker_probabilites) in selected_indices and np.argmax(sentence_probabilites) in [0, 1, 3]):
                self.unlocked()
            else:
                self.locked()

    def predict(self):
        new_recording_path = 'recording.wav'
        new_sentence_features, new_speaker_features = extract_features(new_recording_path)

        predicted_sentence = self.model_sentence.predict_proba([new_sentence_features])
        print(predicted_sentence)
        predicted_speaker = self.model_speaker.predict_proba([new_speaker_features])

        return predicted_sentence, predicted_speaker

if __name__ == "__main__":
    app = QApplication([])
    window = CipherSonicApp()
    window.show()
    app.exec_()
