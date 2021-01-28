import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic, QtCore
import server
import cv2
import threading

# load ui
con_ui = uic.loadUiType("connect.ui")[0]


# ------------------------------------------------
# Thread for changing ui in the while loop
# ------------------------------------------------
class ServerThread(QtCore.QThread):
    # In the thread, we cannot change UI directly.
    # So use signal, and call another function to change ui
    print_signal = pyqtSignal()
    server = None

    # Camera Image List
    frame = None

    def __init__(self, port):
        QtCore.QThread.__init__(self)
        ServerThread.server = server.Server(int(port), 3)

    def run(self):
        while True:
            # To avoid memory exclusive, sleep 10ms
            self.msleep(10)

            ServerThread.frame = ServerThread.server.stream_camera()
            ServerThread.server.send_to_motor(ConnectWindow.speed, ConnectWindow.motor_dir, False)

            # To change GUI, emit signal
            self.print_signal.emit()


# ------------------------------------------------
# GUI
# ------------------------------------------------
class ConnectWindow(QMainWindow, con_ui):
    server = None
    motor_dir = 'l'
    speed = 200

    def __init__(self):
        super(ConnectWindow, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # Connect functions and buttons
        self.conButton.clicked.connect(self.connect)
        self.leftButton.clicked.connect(self.set_left)
        self.rightButton.clicked.connect(self.set_right)
        self.quitButton.clicked.connect(self.quit)
        self.sendButton.clicked.connect(self.set_speed)

        # Set input field's hint
        self.statusText.setText("Status")
        self.portText.setPlaceholderText("Port")
        self.speedText.setPlaceholderText("Speed")

        # Disable buttons, input fields except connect button, port field
        self.speedText.setReadOnly(True)
        self.sendButton.setEnabled(False)
        self.leftButton.setEnabled(False)
        self.rightButton.setEnabled(False)
        self.quitButton.setEnabled(False)

        # Init camera image pixmap
        self.pixmap = None
        self.show()

    def set_img_view(self):
        qImg = list()
        frame = ServerThread.frame
        imgLabels = [self.imgLabel0, self.imgLabel1, self.imgLabel2]

        for i in range(0, len(frame)):
            height, width, channel = frame[i].shape
            bytesPerLine = channel * width

            qImg.append(QImage(frame[i].data, width, height, bytesPerLine, QImage.Format_RGB888))
            # labelName = 'self.imgLabel' + str(i)
        
            self.pixmap = QPixmap.fromImage(qImg[i])
            self.pixmap = self.pixmap.scaled(240, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            imgLabels[i].setPixmap(self.pixmap)

    def set_right(self):
        ConnectWindow.motor_dir = 'r'
        self.statusText.setText("direction : " + ConnectWindow.motor_dir)

    def set_left(self):
        ConnectWindow.motor_dir = 'l'
        self.statusText.setText("direction : " + ConnectWindow.motor_dir)

    def set_speed(self):
        ConnectWindow.speed = int(self.speedText.text())
        self.speedText.setText("")
        self.statusText.setText("speed : " + str(ConnectWindow.speed))

    def quit(self):
        if ServerThread.server is not None:
            ServerThread.server.close()

    def connect(self):
        # self.conButton.setEnabled(False)
        port = self.portText.text()

        # Disable input field
        self.portText.setText("")
        self.statusText.setText("port : " + port)

        self.portText.setReadOnly(True)
        self.speedText.setReadOnly(False)

        self.conButton.setEnabled(False)
        self.sendButton.setEnabled(True)
        self.leftButton.setEnabled(True)
        self.rightButton.setEnabled(True)
        self.quitButton.setEnabled(True)

        # start thread
        self.th = ServerThread(port)
        self.th.print_signal.connect(self.set_img_view)
        self.th.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    connectWindow = ConnectWindow()
    connectWindow.show()
    app.exec_()
