import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql
import random

con = pymysql.connect(host='localhost',
                      user='root',
                      password='',
                      db='tubeshangman')


class mainUI(QMainWindow):
    def __init__(self):
        super(mainUI, self).__init__()
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(700, 650)
        self.initUI()

    def initUI(self):
        self.layoutWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        judul = QLabel(self)
        judul.setPixmap(QPixmap("bg.png"))
        judul.setScaledContents(True)

        self.btnStart = QPushButton('Mulai', self)
        self.btnStart.clicked.connect(self.connectInputName)
        btnScore = QPushButton('Skor', self)
        #statsbtn.clicked.connect()
        btnEdit = QPushButton('Edit', self)
        #editbtn.clicked.connect()
        btnQuit = QPushButton('Keluar', self)
        btnQuit.clicked.connect(quit)

        self.mainLayout.addWidget(judul)
        self.mainLayout.addWidget(self.btnStart)
        self.mainLayout.addWidget(btnScore)
        self.mainLayout.addWidget(btnEdit)
        self.mainLayout.addWidget(btnQuit)

        self.layoutWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.layoutWidget)

    def connectInputName(self):
        self.inputUsername = inputUI()
        self.inputUsername.show()
        self.close()


class inputUI(QMainWindow):
    def __init__(self):
        super(inputUI, self).__init__()
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(300, 100)
        self.inputName()

    def inputName(self):
        self.layoutWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        inputNama = QLineEdit(self)
        self.btnInput = QPushButton("Lanjut", self)
        self.btnInput.clicked.connect(self.connectGame)
        lblName = QLabel("Masukkan Namamu", self)

        self.mainLayout.addWidget(lblName)
        self.mainLayout.addWidget(inputNama)
        self.mainLayout.addWidget(self.btnInput)

        self.layoutWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.layoutWidget)

    def connectGame(self):
        self.game = gameUI()
        self.game.show()
        self.close()


class gameUI(QMainWindow):
    def __init__(self):
        super(gameUI, self).__init__()
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("icon.png"))
        self.theGame()

    def theGame(self):
        self.layoutWidget = QWidget()
        self.mainLayout = QHBoxLayout()
        self.imageLayout = QVBoxLayout()
        self.guessLayout = QVBoxLayout()

        guessWord = self.answerPicker()
        guessWordList = []
        guessQuestion = []
        self.attempt = 9

        for word in guessWord:
            guessWordList.append(word)
        for x in range(len(guessWordList)):
            guessQuestion.append("_")

        #User Interface
        self.lblImage = QLabel("", self)
        self.lblImage.setPixmap(QPixmap(f"gambar/hangman{self.attempt}.png"))
        self.lblQuestion = QLabel("Coba Tebak!!", self)
        self.inputAnswer = QLineEdit(self)
        self.inputAnswer.setMaxLength(1)
        self.btnCheck = QPushButton("Check", self)

        def guessMechanic():
            if self.attempt > 0:
                if guessQuestion == guessWordList:
                    self.msgBoxwin()

                answer = self.inputAnswer.text()

                for i, char in enumerate(guessWordList):
                    if str(answer) == str(char):
                        guessQuestion.pop(i)
                        guessQuestion.insert(i, answer)
                        self.lblQuestion.setText(f"{guessQuestion}")
                if str(answer) not in guessWordList:
                    self.attempt -= 1
                    self.lblImage.setPixmap(
                        QPixmap(f"gambar/hangman{self.attempt}.png"))

                if self.attempt == 0:
                    self.msgBoxlose()

            self.inputAnswer.setText("")

        self.btnCheck.clicked.connect(guessMechanic)

        self.imageLayout.addWidget(self.lblImage)
        self.guessLayout.addWidget(self.lblQuestion)
        self.guessLayout.addWidget(self.inputAnswer)
        self.guessLayout.addWidget(self.btnCheck)

        self.mainLayout.addLayout(self.imageLayout)
        self.mainLayout.addLayout(self.guessLayout)

        self.layoutWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.layoutWidget)

    def answerPicker(self):
        buatsoal = []
        with con.cursor() as x:
            sql = "SELECT*FROM soal"
            x.execute(sql)
            hasil = x.fetchall()
            for x in hasil:
                for y in range(len(x)):
                    buatsoal.append(x[y])
        picker = ''.join(random.choices(buatsoal))
        return picker

    def msgBoxwin(self):
        self.msgBoxwin = QWindow()
        self.show()
        self.setFixedSize(300, 300)
        layoutWidget = QWidget()
        mainLayout = QVBoxLayout()
        btnLayout = QHBoxLayout()

        lblRestart = QLabel("Anda meninggoy")
        btnCobaLagi = QPushButton("Coba Lagi")

        def connectGame():
            game = gameUI()
            self.close()
            game.close()
            game.show()

        btnCobaLagi.clicked.connect(connectGame)
        btnSelesai = QPushButton("Selesai")

        def connectMenu():
            menu = mainUI()
            game = gameUI()
            self.close()
            game.close()
            menu.show()

        btnLayout.addWidget(btnCobaLagi)
        btnLayout.addWidget(btnSelesai)
        mainLayout.addWidget(lblRestart)
        mainLayout.addLayout(btnLayout)
        layoutWidget.setLayout(mainLayout)
        self.setCentralWidget(layoutWidget)

    def msgBoxlose(self):
        self.msgBoxlose = QWindow()
        self.show()
        self.setFixedSize(300, 300)
        layoutWidget = QWidget()
        mainLayout = QVBoxLayout()
        btnLayout = QHBoxLayout()

        lblRestart = QLabel("Anda meninggoy")
        btnCobaLagi = QPushButton("Coba Lagi")

        def connectGame():
            game = gameUI()
            self.close()
            game.close()
            game.show()

        btnCobaLagi.clicked.connect(connectGame)
        btnSelesai = QPushButton("Selesai")

        def connectMenu():
            menu = mainUI()
            game = gameUI()
            self.close()
            game.close()
            menu.show()

        btnLayout.addWidget(btnCobaLagi)
        btnLayout.addWidget(btnSelesai)
        mainLayout.addWidget(lblRestart)
        mainLayout.addLayout(btnLayout)
        layoutWidget.setLayout(mainLayout)
        self.setCentralWidget(layoutWidget)


#class scoreUI():

#class editDatabaseUI():


def exec():
    hangman = QApplication([])
    main = mainUI()
    main.show()
    sys.exit(hangman.exec_())


exec()