import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap
import pymysql

con = pymysql.connect(host='localhost',
                      user='root',
                      password='',
                      db='tubeshangman')

app = QApplication(sys.argv)

class Window(QWidget):

    final = 0

    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setWindowTitle("Hangman")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumSize(QtCore.QSize(700, 650))
        self.setMaximumSize(QtCore.QSize(700, 650))
        
        judul = QLabel(self)
        judul.setPixmap(QPixmap("bg.png"))
        judul.setScaledContents(True)

        startbtn = QPushButton('Mulai', self)
        startbtn.clicked.connect(self.start_to_login)
        statsbtn = QPushButton('Skor', self)
        #statsbtn.clicked.connect()
        editbtn = QPushButton('Edit', self)
        #editbtn.clicked.connect()
        quitbtn = QPushButton ('Keluar', self)
        quitbtn.clicked.connect(quit)
        
        vbox = QVBoxLayout()
        vbox.addWidget(judul)
        vbox.addWidget(startbtn)
        vbox.addWidget(statsbtn)
        vbox.addWidget(editbtn)
        vbox.addWidget(quitbtn)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        self.show()

    def login(self):
        self.setWindowTitle("Masukkan Namamu")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumSize(QtCore.QSize(300, 100))
        self.setMaximumSize(QtCore.QSize(300, 100))
        name = QLineEdit(self)
        enterbtn = QPushButton("Lanjut", self)
        enterbtn.clicked.connect(self.login_to_word)
        lbl1 = QLabel(self)
        lbl1.setText("Masukkan Namamu")

        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addWidget(name)
        vbox.addWidget(enterbtn)
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def login_to_word(self):
        login_window.close()
        word_window.show()

    def quit(self):
        self.QtWidgets.qApp.quit

    def start_to_login(self):
        login_window.show()
        start_window.close()

    def word_to_game(self):
        word_window.close()
        global word_to_guess
        global mask
        word_to_guess = word_by_user.text().upper()

        for i in range(0, len(word_to_guess)):
            mask.append(" _ ")
        word_to_show.setText("".join(mask))
        game_window.show()

    def guessing(self):
        word_to_guess = word_by_user.text().upper()
        if letter_guess.text().upper() in word_to_guess:
            for x in range (0, len(word_to_guess)):
                if letter_guess.text().upper() == word_to_guess[x]:
                    mask[x] = letter_guess.text().upper()

        elif letter_guess.text().upper() not in word_to_guess:
            global attempts
            attempts -=1
            image = QPixmap("gambar\hangman{}.png".format(str(attempts)))
            image_lbl.setPixmap(image)
            if attempts == 0:
                global res_window
                res_window.setWindowTitle("Gagal")
                res_window.setWindowIcon(QIcon("icon.png"))
                res_window.setMinimumSize(QtCore.QSize(300, 100))
                res_window.setMaximumSize(QtCore.QSize(300, 100))
                res_lbl.setText("Kamu kalah!\nCoba lagi?")
                ybtn = QPushButton()
                ybtn.setText("Iya")
                ybtn.clicked.connect(res_window.start_again)
                nbtn = QPushButton()
                nbtn.setText("Tidak")
                nbtn.clicked.connect(quit)
                vbox = QVBoxLayout()
                vbox.addStretch(100)
                vbox.addWidget(res_lbl)
                vbox.addStretch(100)
                hbox = QHBoxLayout()
                hbox.addWidget(ybtn)
                hbox.addWidget(nbtn)
                vbox.addLayout(hbox)
                res_window.setLayout(vbox)
                res_window.show()
        else:
            pass

        word_to_show.setText("".join(mask))
        letter_guess.clear()

        if not " _ " in word_to_show.text().upper():
            res_window.setWindowTitle("Berhasil")
            res_window.setWindowIcon(QIcon("icon.png"))
            res_window.setMinimumSize(QtCore.QSize(300, 100))
            res_window.setMaximumSize(QtCore.QSize(300, 100))
            res_lbl.setText("Kamu menang!\nMain Lagi?")
            ybtn = QPushButton()
            ybtn.setText("Iya")
            ybtn.clicked.connect(res_window.start_again)
            nbtn = QPushButton()
            nbtn.setText("Tidak")
            nbtn.clicked.connect(quit)
            vbox = QVBoxLayout()
            vbox.addStretch(100)
            vbox.addWidget(res_lbl)
            vbox.addStretch(100)
            hbox = QHBoxLayout()
            hbox.addWidget(ybtn)
            hbox.addWidget(nbtn)
            vbox.addLayout(hbox)
            res_window.setLayout(vbox)
            res_window.show()

    def start_again(self):
        global mask
        global attempts
        attempts = 9
        word_by_user.clear()
        word_to_show.setText("")
        mask = []
        game_window.close()
        res_window.close()
        word_window.show()
        image = QPixmap("gambar\hangman9.png")
        image_lbl.setPixmap(image)

attempts = 9
mask = []
word_to_guess = ""
result = 0

start_window = Window()
start_window.initUI()

login_window = Window()
login_window.login()

word_window = Window()
word_window.setWindowTitle("Masukkan Kata")
word_window.setMinimumSize(QtCore.QSize(300, 100))
word_window.setMaximumSize(QtCore.QSize(300, 100))
word_window.setWindowIcon(QIcon("icon.png"))
lbl2 = QLabel(word_window)
lbl2.setText("Masukkan Kata")
word_by_user = QLineEdit(word_window)
nextbtn = QPushButton("Lanjut", word_window)
nextbtn.clicked.connect(Window.word_to_game)
vbox = QVBoxLayout(word_window)
vbox.addWidget(lbl2)
vbox.addWidget(word_by_user)
vbox.addWidget(nextbtn)
hbox = QHBoxLayout()
hbox.addLayout(vbox)
word_window.setLayout(hbox)

game_window = Window()
game_window.setWindowTitle("Hangman")
game_window.setWindowIcon(QIcon("icon.png"))
word_to_show = QLabel(game_window)
letter_guess = QLineEdit(game_window)
letter_guess.setMaxLength(1)
letter_guess.setFixedWidth(100)
tryit = QPushButton (game_window)
tryit.setText("Coba")
tryit.clicked.connect(Window.guessing)
image = QPixmap("gambar\hangman9.png")
image_lbl = QLabel(game_window)
image_lbl.setPixmap(image)
vbox_game = QVBoxLayout(game_window)
vbox_game.addWidget(image_lbl)
vbox_game.addWidget(word_to_show)
vbox_game.addWidget(letter_guess)
vbox_game.addWidget(tryit)
hbox_game = QHBoxLayout(game_window)
hbox_game.addLayout(vbox_game)
game_window.setLayout(hbox_game)

res_window = Window()
res_lbl = QLabel(res_window)

sys.exit(app.exec_())