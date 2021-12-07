import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
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
        self.setWindowIcon(QIcon("gambar/icon.png"))
        self.setFixedSize(700, 650)
        self.initUI()

        tutorialAct = QAction('&Cara Bermain', self)
        tutorialAct.setStatusTip('Tutorial Bermain Hangman')
        tutorialAct.triggered.connect(self.connectTutor)

        creditsAct = QAction('&Credits', self)
        creditsAct.setStatusTip('Pembuat Aplikasi')
        creditsAct.triggered.connect(self.connectCredit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Informasi')
        fileMenu.addAction(tutorialAct)
        fileMenu.addAction(creditsAct)

    def initUI(self):
        self.layoutWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        judul = QLabel(self)
        judul.setPixmap(QPixmap("gambar/bg.png"))

        self.btnStart = QPushButton('Mulai', self)
        self.btnStart.clicked.connect(self.connectInputName)
        btnScore = QPushButton('Skor', self)
        #statsbtn.clicked.connect()
        self.btnEdit = QPushButton('Edit', self)
        self.btnEdit.clicked.connect(self.connectTambahSoal)
        btnQuit = QPushButton('Keluar', self)
        btnQuit.clicked.connect(quit)

        self.mainLayout.addWidget(judul)
        self.mainLayout.addWidget(self.btnStart)
        self.mainLayout.addWidget(btnScore)
        self.mainLayout.addWidget(self.btnEdit)
        self.mainLayout.addWidget(btnQuit)

        self.layoutWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.layoutWidget)

    def connectInputName(self):
        self.inputUsername = inputUI()
        self.inputUsername.show()
        self.close()

    def connectTambahSoal(self):
        self.inputSoal = editDatabaseUI()
        self.inputSoal.show()
        self.close()

    def connectCredit(self):
        self.infoCredit = creditUI()
        self.infoCredit.show()
        self.close()

    def connectTutor(self):
        self.infoTutor = tutorialUI()
        self.infoTutor.show()
        self.close()


class tutorialUI(QMainWindow):
    def __init__(self):
        super(tutorialUI, self).__init__()
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("gambar/icon.png"))
        self.setFixedSize(700, 650)
        self.tutor()

    def tutor(self):
        self.layoutWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        judul = QLabel(self)
        judul.setPixmap(QPixmap("gambar/tutorial.png"))

        self.mainLayout.addWidget(judul)
        self.layoutWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.layoutWidget)

    def closeEvent(self, closeEvent):
        self.menu = mainUI()
        self.close()
        self.menu.show()


class creditUI(QMainWindow):
    def __init__(self):
        super(creditUI, self).__init__()
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("gambar/icon.png"))
        self.setFixedSize(700, 650)
        self.pembuat()

    def pembuat(self):
        self.layoutWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        judul = QLabel(self)
        judul.setPixmap(QPixmap("gambar/credits.png"))

        self.mainLayout.addWidget(judul)
        self.layoutWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.layoutWidget)

    def closeEvent(self, closeEvent):
        self.menu = mainUI()
        self.close()
        self.menu.show()


class inputUI(QMainWindow):
    def __init__(self):
        super(inputUI, self).__init__()
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("gambar/icon.png"))
        self.setFixedSize(300, 100)
        self.inputName()

    def inputName(self):
        self.layoutWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        self.inputNama = QLineEdit(self)
        self.btnInput = QPushButton("Lanjut", self)
        self.btnInput.clicked.connect(self.connectGame)
        lblName = QLabel("Masukkan Namamu", self)

        self.mainLayout.addWidget(lblName)
        self.mainLayout.addWidget(self.inputNama)
        self.mainLayout.addWidget(self.btnInput)

        self.layoutWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.layoutWidget)

    def getUsername(self):
        nama = str(self.inputNama.text())
        return nama

    def connectGame(self):
        self.getUsername()
        with con.cursor() as x:
            nama = self.getUsername()
            query = "INSERT INTO skor (skor_nama) VALUES (%s)"
            x.execute(query, nama)
            con.commit()
        print(self.getUsername())
        self.game = gameUI()
        self.game.show()
        self.close()


class gameUI(QMainWindow):
    def __init__(self):
        super(gameUI, self).__init__()
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("gambar/icon.png"))
        self.setFixedSize(700, 500)
        self.theGame()

    def theGame(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

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
        with con.cursor() as x:
            queryA = "SELECT ID_skor FROM skor"
            x.execute(queryA)
            self.latestID = len(x.fetchall())
            queryB = "SELECT skor_catat FROM skor WHERE skor.ID_skor = %s"
            data = (self.latestID)
            x.execute(queryB, data)
            hasilQuery = x.fetchall()
            self.skor = hasilQuery[-1]
            for x in self.skor:
                self.skor = x

        #User Interface
        self.lblImage = QLabel("", self)
        self.lblImage.setPixmap(QPixmap(f"gambar/hangman{self.attempt}.png"))
        pemisah = "  "
        self.lblQuestion = QLabel(pemisah.join(guessQuestion), self)
        self.lblQuestion.setFont(font)
        self.inputAnswer = QLineEdit(self)
        self.inputAnswer.setMaxLength(1)
        self.btnCheck = QPushButton("Check", self)

        def guessMechanic():
            if self.attempt > 0:
                answer = self.inputAnswer.text().upper()

                for i, char in enumerate(guessWordList):
                    if str(answer).upper() == str(char).upper():
                        guessQuestion.pop(i).upper()
                        guessQuestion.insert(i, answer)
                        self.lblQuestion.setText(pemisah.join(guessQuestion))
                if str(answer).upper() not in str(guessWordList).upper():
                    self.attempt -= 1
                    self.lblImage.setPixmap(
                        QPixmap(f"gambar/hangman{self.attempt}.png"))

                if str(guessQuestion).upper() == str(guessWordList).upper():
                    self.msgBoxwin()

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
            query = "SELECT kata FROM soal"
            x.execute(query)
            hasil = x.fetchall()
            for x in hasil:
                for y in range(len(x)):
                    buatsoal.append(x[y])
        picker = ''.join(random.choices(buatsoal))
        return picker

    def msgBoxwin(self):
        with con.cursor() as x:
            query = "UPDATE skor SET skor_catat = %s WHERE skor.ID_skor = %s"
            self.skor += int(100)
            data = (self.skor, self.latestID)
            x.execute(query, data)
            con.commit()

        self.msgBoxwin = QWindow()
        self.show()
        self.setFixedSize(700, 500)
        layoutWidget = QWidget()
        mainLayout = QVBoxLayout()
        secondLayout = QHBoxLayout()
        btnLayout = QHBoxLayout()

        btnCobaLagi = QPushButton("Main Lagi")

        gifWin = QMovie("gambar/win.gif")
        winImage = QLabel(self)
        winImage.setMovie(gifWin)
        gifWin.start()

        gifWin2 = QMovie("gambar/menang.gif")
        winImage2 = QLabel(self)
        winImage2.setMovie(gifWin2)
        gifWin2.start()

        def connectGame():
            menu = gameUI()
            self.close()
            menu.show()

        btnCobaLagi.clicked.connect(connectGame)

        def connectMenu():
            menu = mainUI()
            self.close()
            menu.show()

        btnSelesai = QPushButton("Selesai")
        btnSelesai.clicked.connect(connectMenu)

        btnLayout.addWidget(btnCobaLagi)
        btnLayout.addWidget(btnSelesai)
        secondLayout.addWidget(winImage)
        secondLayout.addWidget(winImage2)
        mainLayout.addLayout(secondLayout)
        mainLayout.addLayout(btnLayout)
        layoutWidget.setLayout(mainLayout)
        self.setCentralWidget(layoutWidget)

    def msgBoxlose(self):
        self.msgBoxlose = QWindow()
        self.show()
        self.setFixedSize(700, 500)
        layoutWidget = QWidget()
        mainLayout = QVBoxLayout()
        secondLayout = QHBoxLayout()
        btnLayout = QHBoxLayout()

        btnCobaLagi = QPushButton("Coba Lagi")
        loseImage = QLabel("", self)
        loseImage.setPixmap(QPixmap("gambar/hangman0.png"))

        gifLose = QMovie("gambar/kalah.gif")
        loseImage2 = QLabel(self)
        loseImage2.setMovie(gifLose)
        gifLose.start()

        def connectGame():
            game = gameUI()
            self.close()
            game.close()
            game.show()

        btnCobaLagi.clicked.connect(connectGame)

        def connectMenu():
            menu = mainUI()
            game = gameUI()
            menu.show()
            self.close()
            game.close()

        btnSelesai = QPushButton("Selesai")
        btnSelesai.clicked.connect(connectMenu)

        btnLayout.addWidget(btnCobaLagi)
        btnLayout.addWidget(btnSelesai)
        secondLayout.addWidget(loseImage)
        secondLayout.addWidget(loseImage2)
        mainLayout.addLayout(secondLayout)
        mainLayout.addLayout(btnLayout)
        layoutWidget.setLayout(mainLayout)
        self.setCentralWidget(layoutWidget)


#class scoreUI():


class editDatabaseUI(QMainWindow):
    def __init__(self):
        super(editDatabaseUI, self).__init__()
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("gambar/icon.png"))
        self.setFixedSize(700, 700)
        self.tambahSoal()

    def tambahSoal(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        layoutWidget = QWidget()
        mainLayout = QHBoxLayout()
        kiriLayout = QVBoxLayout()
        kananLayout = QVBoxLayout()

        lblSoal = QLabel("Daftar Kunci Jawaban", self)
        lblSoal.setFont(font)
        lblSoal.setAlignment(Qt.AlignCenter)
        self.tableView = QTableWidget()
        self.tableView.setColumnCount(1)
        self.tableView.setHorizontalHeaderLabels(["Kata"])
        self.tableView.setColumnWidth(0, 325)

        def loaddata():
            with con.cursor() as x:
                query = "SELECT * FROM soal"
                x.execute(query)
                hasil = x.fetchall()
                rowsCount = len(hasil)
                self.tableView.setRowCount(rowsCount)
                tableRow = -1
                for x in hasil:
                    self.tableView.setItem(tableRow, 1, QTableWidgetItem(x[0]))
                    tableRow += 1

        loaddata()

        lblTanya = QLabel("Masukkan Soal Baru", self)
        lblTanya.setFont(font)
        lblTanya.setAlignment(Qt.AlignCenter)
        lblFB = QLabel("", self)
        inputSoal = QLineEdit(self)
        btnTambah = QPushButton("Tambah", self)
        btnHapus = QPushButton("Hapus", self)

        def klikTambah():
            Question = inputSoal.text().lower()
            with con.cursor() as x:
                query = "INSERT INTO soal (kata) VALUES (%s)"
                data = (Question)
                x.execute(query, data)
                lblFB.setText("Data Berhasil Dimasukkan")
                lblFB.setAlignment(Qt.AlignCenter)
                con.commit()
                loaddata()

        def klikHapus():
            Question = inputSoal.text().lower()
            with con.cursor() as x:
                query = "DELETE FROM soal WHERE soal.kata = %s"
                data = (Question)
                x.execute(query, data)
                lblFB.setText("Data Berhasil Dihapus")
                lblFB.setAlignment(Qt.AlignCenter)
                con.commit()
                loaddata()

        btnTambah.clicked.connect(klikTambah)
        btnHapus.clicked.connect(klikHapus)

        kiriLayout.addWidget(lblSoal)
        kiriLayout.addWidget(self.tableView)
        kananLayout.addWidget(lblFB)
        kananLayout.addWidget(lblTanya)
        kananLayout.addWidget(inputSoal)
        kananLayout.addWidget(btnTambah)
        kananLayout.addWidget(btnHapus)
        mainLayout.addLayout(kiriLayout)
        mainLayout.addLayout(kananLayout)

        layoutWidget.setLayout(mainLayout)
        self.setCentralWidget(layoutWidget)

    def closeEvent(self, closeEvent):
        self.menu = mainUI()
        self.close()
        self.menu.show()


def exec():
    hangman = QApplication([])
    main = mainUI()
    main.show()
    sys.exit(hangman.exec_())


exec()