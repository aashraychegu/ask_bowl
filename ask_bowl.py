from ask_bowl_web_retrieval import *
from ask_bowl_widgets import *

try:
    # Include in try/except block if you're also targeting Mac/Linux
    # ..or..
    import ctypes

    myappid = "com.SomeStudio.Ask_Bowl.Desktop.21"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        self.curr_question = None
        super().__init__(*args, **kwargs)

        width = 800
        height = 450

        # setting the minimum size
        self.setMinimumSize(width, height)
        self.istup = True
        self.isanswered, self.isranswered = False, False
        self.isread = 0
        container = QWidget()
        layout = QHBoxLayout()
        self.actions = action_bar()
        layout.addWidget(self.actions)
        self.text = show_area()
        layout.addWidget(self.text)
        self.answerpane = answerbox()
        layout.addWidget(self.answerpane)
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.text)

        self.scroll1 = QScrollArea()
        self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll1.setWidgetResizable(True)
        self.scroll1.setWidget(self.actions)

        self.scroll2 = QScrollArea()
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.answerpane)

        layout.addWidget(self.scroll1)
        layout.addWidget(self.scroll)
        layout.addWidget(self.scroll2)
        self.actions.nextbtn.clicked.connect(self.on_next_clicked)
        self.actions.startbtn.clicked.connect(self.on_start_clicked)
        self.actions.answer.clicked.connect(self.on_answer_clicked)
        self.actions.repeatallbtn.clicked.connect(self.repeat)
        self.actions.alltext.clicked.connect(self.set_all_visibility)
        self.actions.questiontext.clicked.connect(self.set_question_visibility)
        self.actions.answertext.clicked.connect(self.set_answer_visibility)
        self.actions.reviewbtn.clicked.connect(self.review_clicked)
        self.answerpane.abox.editingFinished.connect(self.answered)
        self.answerpane.done.clicked.connect(self.answered)
        self.answerpane.correct.clicked.connect(self.c)
        self.answerpane.wrong.clicked.connect(self.w)
        try:
            engineNames = QTextToSpeech.availableEngines()
            engineName = engineNames[0]
        except:
            engineName = "sapi"
        self.engine = QTextToSpeech(engineName)
        self.engine.stateChanged.connect(self.stateChanged)
        self.voices = []
        vlist = self.engine.availableVoices()
        for voice in vlist:
            self.voices.append(voice)
            self.actions.voiceCombo.addItem(voice.name())
        self.engine.stateChanged.connect(self.stateChanged)
        self.set_question()
        self.actions.setvalidity(True)
        self.resize(800, 398)
        self.actions.pausebtn.clicked.connect(self.pause)
        self.actions.playbtn.clicked.connect(self.play)
        self.actions.stopbtn.clicked.connect(self.engine.stop)
        self.amap = {
            "s": self.on_start_clicked,
            "n": self.on_next_clicked,
            "t": self.engine.stop,
            " ": self.on_space_pressed,
            "r": self.review_clicked,
            "a": self.on_answer_clicked,
            "q": self.on_question_clicked,
            "l": self.set_all_visibility,
            "u": self.set_question_visibility,
            "n": self.set_answer_visibility,
            "d": self.answerpane.abox.setFocus,
            "c": self.c,
            "w": self.w,
        }
        self.actions.nextbtn.setEnabled(False)

    def on_space_pressed(self):
        if self.engine.State.Speaking:
            self.engine.pause()
        else:
            self.engine.resume()

    def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        try:
            (self.amap[chr(event.key()).lower()]())
        except:
            ...
        return super().keyPressEvent(event)

    def play(self):
        self.engine.resume()

    def pause(self):
        self.engine.pause()

    def c(self):
        if self.isranswered or self.isanswered == False:
            return 0

        self.answerpane.wnum -= 1
        self.answerpane.cnum += 1
        self.answerpane.cwtext.setText("<h2>Correct: " +
                                       str(self.answerpane.cnum) +
                                       " Incorrect: " +
                                       str(self.answerpane.wnum))
        self.isranswered = True

    def w(self):
        if self.isranswered or self.isanswered == False:
            return 0

        self.answerpane.wnum -= -1
        self.answerpane.cnum += -1
        self.answerpane.cwtext.setText("<h2>Correct: " +
                                       str(self.answerpane.cnum) +
                                       " Incorrect: " +
                                       str(self.answerpane.wnum))
        self.isranswered = True

    def saying(func):
        def inner(self):
            self.actions.setvalidity(False)
            func(self)

        return inner

    @saying
    def on_start_clicked(self):
        self.engine.stop()
        self.isanswered, self.isranswered = False, False
        if self.isread != 2:
            self.isread += 1
        self.set_engine_properties()
        if self.istup:
            self.engine.say(self.curr_question.tossup.q)
        else:
            self.engine.say(self.curr_question.bonus.q)
        self.istup = not self.istup
        if not self.istup:
            self.actions.nextbtn.setEnabled(False)
        else:
            self.actions.nextbtn.setEnabled(True)
        self.isread %= 3

    def on_next_clicked(self):
        self.engine.stop()
        self.isanswered, self.isranswered = False, False
        self.isread += 1
        self.isread %= 3
        if self.isread == 0:
            self.set_question()
            self.actions.nextbtn.setEnabled(False)
            self.istup = True
            self.isread = 0
        else:
            self.istup = not self.istup

    def get_question(self):
        self.curr_question = make_new_question()
        _title = "ask_bowl: Question ID " + str(
            self.curr_question.link).replace("https://scibowldb.com/tossup/",
                                             "")
        self.setWindowTitle(_title)
        self.answerpane.abox.setText("")

    def set_question(self):
        self.get_question()

        self.text.Tquestion_text.setVisible(False)
        self.text.Tanswer_text.setVisible(False)
        self.text.Bquestion_text.setVisible(False)
        self.text.Banswer_text.setVisible(False)
        self.text.Tquestion_text.setText(self.curr_question.tossup.q)
        self.text.Tanswer_text.setText(self.curr_question.tossup.ans)
        self.text.Bquestion_text.setText(self.curr_question.bonus.q)
        self.text.Banswer_text.setText(self.curr_question.bonus.ans)
        self.text.Tquestion_text.setVisible(False)
        self.text.Tanswer_text.setVisible(False)
        self.text.Bquestion_text.setVisible(False)
        self.text.Banswer_text.setVisible(False)
        _title = "ask_bowl: Question ID " + str(
            self.curr_question.link).replace("https://scibowldb.com/tossup/",
                                             "")
        self.setWindowTitle(_title)

    def set_all_visibility(self, ):
        self.text.Tquestion_text.setVisible(True)
        self.text.Tanswer_text.setVisible(True)
        self.text.Bquestion_text.setVisible(True)
        self.text.Banswer_text.setVisible(True)

    def set_question_visibility(self, ):

        # self.istup = not self.istup
        if self.isread == 1:
            self.text.Tquestion_text.setVisible(True)
        elif self.isread == 2:
            self.text.Bquestion_text.setVisible(True)
        # self.istup = not self.istup

    def set_answer_visibility(self, ):
        # self.istup = not self.istup
        if self.isread == 1:
            self.text.Tanswer_text.setVisible(True)
        if self.isread == 2:
            self.text.Banswer_text.setVisible(True)
        # self.istup = not self.istup

    @saying
    def repeat(self, elements="ALL"):
        if self.isread == 1:
            self.istup = not self.istup
        self.on_start_clicked()

    def stateChanged(self, state):
        if state == QTextToSpeech.State.Ready:
            self.actions.setvalidity(True)

    @saying
    def on_answer_clicked(self):
        if self.isread > 0:
            self.istup = not self.istup
        self.set_engine_properties()
        if self.istup:
            self.engine.say(self.curr_question.tossup.ans)
        else:
            self.engine.say(self.curr_question.bonus.ans)
        if self.isread > 0:
            self.istup = not self.istup

    @saying
    def on_question_clicked(self):
        self.set_engine_properties()
        self.istup = not self.istup
        if self.isread == 1:
            self.engine.say(self.curr_question.tossup.ans)
        else:
            self.engine.say(self.curr_question.bonus.ans)
        self.istup = not self.istup

    def answered(self):
        self.engine.pause()
        if self.isread == 0:
            return None
        if self.isanswered:
            return None
        self.istup = not self.istup
        if self.istup:
            item = self.curr_question.tossup
        else:
            item = self.curr_question.bonus

        if item.isMC:
            if self.checkMC(item) == 0:
                self.engine.resume()
        else:
            if self.checkSA(item) == 0:
                self.engine.resume()

        self.answerpane.cwtext.setText("<h2>Correct: " +
                                       str(self.answerpane.cnum) +
                                       " Incorrect: " +
                                       str(self.answerpane.wnum))
        self.istup = not self.istup
        self.isanswered = True
        self.engine.stop()
        self.on_answer_clicked()
        if self.istup:
            self.text.istossup.setText("<b><h2>Current Question: Tossup")
        else:
            self.text.istossup.setText("<b><h2>Current Question: Bonus")

    def checkMC(self, item):
        if self.answerpane.abox.text().lower() == item.ans[0].lower():
            self.answerpane.cnum += 1
            self.engine.resume()
            self.engine.stop()
            self.answerpane.abox.setText("")
            return 1
        else:
            self.answerpane.wnum += 1
            return 0

    def checkSA(self, item):
        if (QMessageBox.question(
                self,
                "Is your Answer Correct?",
                "Are these two the same: " + item.ans + " and: " +
                self.answerpane.abox.text(),
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes,
        ) == QMessageBox.Yes):
            self.answerpane.cnum += 1
            self.engine.resume()
            self.engine.stop()
            self.answerpane.abox.setText("")

        else:
            self.answerpane.wnum += 1
            return 0

    def review_clicked(self):
        webbrowser.open_new_tab(self.curr_question.link)

    def set_engine_properties(self):
        self.engine.setVoice(
            self.voices[self.actions.voiceCombo.currentIndex()])
        self.engine.setVolume(self.actions.voiceVolume.value())
        self.engine.setRate(self.actions.voiceRate.value())
        self.engine.setPitch(self.actions.voicePitch.value())


app = QApplication(sys.argv)
splash_pix = QPixmap(
    "resources/book_education_growth_biology_science_icon_124783.png")
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
splash.setMask(splash_pix.mask())
splash.show()
QLabel("loading latest questions").show()
app.processEvents()
app.setWindowIcon(QtGui.QIcon("resources/icon.ico"))
w = MainWindow()
w.show()
splash.finish(w)
sys.exit(app.exec())
