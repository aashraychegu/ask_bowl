from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import PySide6
import sys

try:
    from PySide6.QtTextToSpeech import QTextToSpeech
except ImportError:
    from PySide2.QtTextToSpeech import QTextToSpeech


class action_bar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        h = 30
        v = 35
        self.startbtn = QPushButton("&Start")
        self.nextbtn = QPushButton("&Next Question")
        self.pausebtn = QPushButton("Pause (Spacebar)")
        self.playbtn = QPushButton("Play (Spacebar)")
        self.stopbtn = QPushButton("S&top")
        self.answer = QPushButton("S&ay Answer")
        self.repeatallbtn = QPushButton("Repeat &Question")
        self.alltext = QPushButton("Show A&ll Text")
        self.questiontext = QPushButton("Show Q&uestion Text")
        self.answertext = QPushButton("Show A&nswer Text")
        self.reviewbtn = QPushButton("&Review")
        self.voiceCombo = QComboBox()
        self.voicePitch = QDoubleSpinBox()
        self.voiceRate = QDoubleSpinBox()
        self.voiceVolume = QDoubleSpinBox()

        (self.voiceRate).setRange(-1, 1)
        (self.voiceVolume).setRange(0, 1)
        self.voicePitch.setRange(-1, 1)
        self.voiceRate.setSingleStep(0.01)
        self.voiceVolume.setSingleStep(0.01)
        self.voicePitch.setSingleStep(0.1)
        self.voiceVolume.setValue(1)
        self.voiceRate.setValue(0.0)
        self.voicePitch.setValue(0.0)
        layout.addWidget(self.startbtn)
        layout.addWidget(self.nextbtn)
        layout.addWidget(self.pausebtn)
        layout.addWidget(self.playbtn)
        layout.addWidget(self.stopbtn)
        layout.addWidget(self.reviewbtn)
        layout.addWidget(self.answer)
        layout.addWidget(self.repeatallbtn)
        layout.addWidget(self.alltext)
        layout.addWidget(self.questiontext)
        layout.addWidget(self.answertext)
        layout.addWidget(QLabel("<h4>Voice Settings:"))
        layout.addWidget(QLabel("<h6>Voice Type:"))
        layout.addWidget(self.voiceCombo)
        layout.addWidget(QLabel("<h6>Volume:"))
        layout.addWidget(self.voiceVolume)
        layout.addWidget(QLabel("<h6>Rate\Speed:"))
        layout.addWidget(self.voiceRate)
        layout.addWidget(QLabel("<h6>Pitch:"))
        layout.addWidget(self.voicePitch)
        (self.startbtn).setMinimumSize(h, v)
        (self.nextbtn).setMinimumSize(h, v)
        (self.answer).setMinimumSize(h, v)
        (self.stopbtn).setMinimumSize(h, v)
        (self.repeatallbtn).setMinimumSize(h, v)
        (self.alltext).setMinimumSize(h, v)
        (self.questiontext).setMinimumSize(h, v)
        (self.answertext).setMinimumSize(h, v)
        (self.reviewbtn).setMinimumSize(h, v)
        (self.pausebtn).setMinimumSize(h, v)
        (self.playbtn).setMinimumSize(h, v)
        (self.voiceCombo).setMinimumSize(h, v)
        self.voiceVolume.setMinimumSize(h, v)
        self.voiceRate.setMinimumSize(h, v)
        self.voicePitch.setMinimumSize(h, v)
        self.setLayout(layout)

    def setvalidity(self, tof):
        (self.startbtn).setEnabled(tof)
        (self.nextbtn).setEnabled(tof)
        (self.answer).setEnabled(tof)
        (self.repeatallbtn).setEnabled(tof)
        # (self.alltext).setEnabled(tof)
        # (self.questiontext).setEnabled(tof)
        # (self.answertext).setEnabled(tof)
        # (self.voiceCombo).setEnabled(tof)


class show_area(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.istossup = QLabel("<b><h2>Current Question: Tossup")
        self.Tquestion_text = QLabel()
        self.Tquestion_text.setWordWrap(True)
        self.Tanswer_text = QLabel()
        self.Tanswer_text.setWordWrap(True)
        self.Bquestion_text = QLabel()
        self.Bquestion_text.setWordWrap(True)
        self.Bquestion_text.setStyleSheet("margin-top: 10%")
        self.Banswer_text = QLabel()
        self.Banswer_text.setWordWrap(True)
        layout.addWidget(self.istossup)
        layout.addWidget(QLabel("<h3>Tossup Question:"))
        layout.addWidget(self.Tquestion_text)
        layout.addWidget(QLabel("<h3>Tossup Answer:"))
        layout.addWidget(self.Tanswer_text)
        layout.addWidget(QLabel("<h3>Bonus Question:"))
        layout.addWidget(self.Bquestion_text)
        layout.addWidget(QLabel("<h3>Bonus Answer:"))
        layout.addWidget(self.Banswer_text)
        self.Tquestion_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.Tanswer_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.Bquestion_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.Banswer_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setLayout(layout)


class answerbox(QWidget):
    def __init__(self):
        super().__init__()

        h = 30
        v = 35
        self.layout = QVBoxLayout()
        self.cnum = 0
        self.wnum = 0
        # self.timer = QLabel("<h1> -:-/-:-")
        # self.layout.addWidget(self.timer)
        self.cwtext = QLabel("<h2>Correct: " + str(self.cnum) +
                             " Incorrect: " + str(self.wnum))
        self.cwtext.setWordWrap(True)
        self.layout.addWidget(self.cwtext)
        ins = QLabel(
            "Enter your answer below. The algorithm will attempt to check if the answer is correct. For multiple choice questions, just type in the letter. For multi select, seperate your answers with spaces."
        )
        ins.setWordWrap(True)
        self.abox = QLineEdit()
        self.abox.setGeometry(1, 1, 30, 30)
        self.abox.setClearButtonEnabled(True)
        self.feedback = QLabel
        self.done = QPushButton("&Done")
        self.correct = QPushButton("I was &correct")
        self.wrong = QPushButton("I was &wrong")
        self.layout.addWidget(ins)
        self.layout.addWidget(self.abox)
        self.layout.addWidget(self.done)
        self.layout.addWidget(self.correct)
        self.layout.addWidget(self.wrong)
        self.abox.setMinimumSize(h, v)
        self.done.setMinimumSize(h, v)
        self.correct.setMinimumSize(h, v)
        self.wrong.setMinimumSize(h, v)
        self.setLayout(self.layout)
        self.setGeometry(30, 1, 30, 398)
        self.resize(30, 398)
