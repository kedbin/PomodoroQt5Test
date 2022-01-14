#!/usr/bin/python3
import os
import platform
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.currentDir = os.path.dirname(__file__)
        self.setWindowTitle("Kedbin's Pomodoro App")

        self.counter = 0

        self.startBtn=QPushButton('Start')
        self.endBtn=QPushButton('Stop')
        self.breakBtn=QPushButton('Break')

        self.layout = QGridLayout()

        fnt = QFont('Helvetica', 20)

        self.lbl = QLabel()
        self.lbl.setFont(fnt)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setText(f"Pomodoro App!")

        self.layout.addWidget(self.lbl,0,0,1,2)
        self.layout.addWidget(self.startBtn,1,0)
        self.layout.addWidget(self.endBtn,1,1)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)

        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
        self.breakBtn.clicked.connect(self.breakTimer)

        self.prevReward = ""

    def displayTime(self):
        self.resize(self.sizeHint())
        if platform.system() == "Windows":
            self.displayTimeWin()
            return
        if self.pomodoro == 0:
            if self.counter % 4 == 0:
                self.lbl.setText(f"You have completed {self.counter} Pomodoros \
\n You are given a 30 minute break!")
            else:
                self.lbl.setText(f"Time's Up! This is Pomodoro # {self.counter}")
            if self.Reward == 1:
                files = [f for f in os.listdir(f"{self.currentDir}/Reward") if os.path.isfile(f"{self.currentDir}/Reward/{f}")]
                file = random.choice(files)
                while self.prevReward == file:
                    file = random.choice(files)
                vlcCommand = f"{self.currentDir}/Reward/\"{file}\" vlc://quit"
                self.prevReward = file
                self.Reward = 0
            elif self.Restart == 1:
                files = [f for f in os.listdir(f"{self.currentDir}/Restart") if os.path.isfile(f"{self.currentDir}/Restart/{f}")]
                file = random.choice(files)
                vlcCommand = f"{self.currentDir}/Restart/\"{file}\" -L -f"
                self.Restart = 0
            os.system(f"vlc {vlcCommand} > /dev/null 2>&1 &")
            self.layout.addWidget(self.breakBtn,2,0,1,2)
            self.startBtn.setEnabled(True)
            self.breakBtn.setEnabled(True)
            self.endBtn.setEnabled(False)
            self.timer.stop()
            return
        mins = int(self.pomodoro // 60)
        sec = int(self.pomodoro % 60)

        displayText = f"{mins}:{sec}"

        self.lbl.setText(displayText)

        self.pomodoro -=1

    def startTimer(self):
        self.setWindowOpacity(1) 
        self.pomodoro = 0.1*60
        self.timer.start(1000)
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)
        self.breakBtn.setEnabled(False)
        self.counter += 1
        self.Reward = 1

    def endTimer(self):
        self.timer.stop()
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)

    def breakTimer(self):
        if self.counter > 0 and self.counter % 4 == 0:
            self.pomodoro = 30*60
        else:
            self.pomodoro = 0.1*60
        self.timer.start(1000)
        self.startBtn.setEnabled(False)
        self.breakBtn.setEnabled(False)
        self.Restart = 1

    def displayTimeWin(self):
        if self.pomodoro == 0:
            if self.counter % 4 == 0:
                self.lbl.setText(f"You have completed {self.counter} Pomodoros \
\n You are given a 30 minute break!")
            else:
                self.lbl.setText(f"Time's Up! This is Pomodoro # {self.counter}")
            if self.Reward == 1:
                files = [f for f in os.listdir(f"{self.currentDir}\\Reward") if os.path.isfile(f"{self.currentDir}\\Reward\\{f}")]
                file = random.choice(files)
                while self.prevReward == file:
                    file = random.choice(files)
                self.prevReward = file
                vlcCommand = f"{self.currentDir}\\Reward\\\"{file}\""
                self.Reward = 0
            elif self.Restart == 1:
                files = [f for f in os.listdir(f"{self.currentDir}\\Restart") if os.path.isfile(f"{self.currentDir}\\Restart\\{f}")]
                file = random.choice(files)
                vlcCommand = f"{self.currentDir}\\Restart\\\"{file}\""
                self.Restart = 0
            os.system(f"{vlcCommand}")
            self.layout.addWidget(self.breakBtn,2,0,1,2)
            self.startBtn.setEnabled(True)
            self.breakBtn.setEnabled(True)
            self.endBtn.setEnabled(False)
            self.timer.stop()
            return
        mins = int(self.pomodoro // 60)
        sec = int(self.pomodoro % 60)

        displayText = f"{mins}:{sec}"

        self.lbl.setText(displayText)

        self.pomodoro -=1



if __name__ == "__main__":
    app = QApplication([])
    demo = AppDemo()
    demo.show()

    app.exec_()
