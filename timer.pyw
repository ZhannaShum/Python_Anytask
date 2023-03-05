import sys
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, \
    QMainWindow, QPushButton, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class CountdownTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timer")

        # Устанавливаем UI
        self.initUI()

    def initUI(self):
        time_label = QLabel("Time:")
        self.time_edit = QLineEdit()
        self.display_label = QLabel("00:00")
        start_button = QPushButton("Start")
        pause_button = QPushButton("Pause")
        stop_button = QPushButton("Stop")
        sound_label = QLabel("Sound:")
        self.sound_edit = QLineEdit()
        self.sound_edit.setText("sound.mp3")

        layout = QGridLayout()
        layout.addWidget(time_label, 0, 0)
        layout.addWidget(self.time_edit, 0, 1)
        layout.addWidget(self.display_label, 0, 2)
        layout.addWidget(start_button, 1, 0)
        layout.addWidget(pause_button, 1, 1)
        layout.addWidget(stop_button, 1, 2)
        layout.addWidget(sound_label, 2, 0)
        layout.addWidget(self.sound_edit, 2, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Присоединяем сигналы к слотам
        start_button.clicked.connect(self.start)
        pause_button.clicked.connect(self.pause)
        stop_button.clicked.connect(self.stop)

        # Инициализация таймера
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)

        self.is_paused = False
        self.elapsed_time = 0
        # Инициализация плеера для аудио
        self.player = QMediaPlayer()

    def start(self):
        time = QTime.fromString(self.time_edit.text(), "mm:ss")
        if not time.isValid():
            self.display_label.setText("Invalid time. Example: 00:05")
            return

        # Получаем время таймера
        self.seconds_remaining = time.minute() * 60 + time.second()

        # Обновляем отображение таймера на форме
        self.update_display()
        self.timer.start(1000)
        self.player.setMedia(
            QMediaContent(QUrl.fromLocalFile(self.sound_edit.text())))
        self.player.stop()

    def pause(self):
        if not self.is_paused:
            # Обработка паузы
            self.timer.stop()
            self.elapsed_time = self.seconds_remaining
            self.is_paused = True
        else:
            self.timer.start(1000)
            self.seconds_remaining = self.elapsed_time
            self.is_paused = False

        self.update_display()

    def stop(self):
        # Остановка таймера, ресет информации на форме
        self.timer.stop()
        self.display_label.setText("00:00")
        self.seconds_remaining = 0
        self.elapsed_time = 0
        self.player.stop()

    def update_display(self):
        # Обновление информации на экране
        self.seconds_remaining -= 1
        minutes = self.seconds_remaining // 60
        seconds = self.seconds_remaining % 60
        self.display_label.setText("{:02d}:{:02d}".format(minutes, seconds))

        # Проверка на окончание таймера
        if self.seconds_remaining <= 0:
            self.player.play()
            self.timer.stop()
            self.display_label.setText("00:00")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = CountdownTimer()
    timer.show()
    sys.exit(app.exec_())
