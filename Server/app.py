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
# For camera image
# ------------------------------------------------
class ServerThread(QtCore.QThread):
    # In the thread, we cannot change UI directly.
    # So use signal, and call another function to change ui
    print_signal = pyqtSignal()
    server = None

    frame = None
    frame2 = None
    frame3 = None

    def __init__(self, port):
        QtCore.QThread.__init__(self)
        ServerThread.server = server.Server(int(port))

    def run(self):
        while True:
            # To avoid memory exclusive, sleep 10ms
            self.msleep(10)
            ServerThread.frame = ServerThread.server.get_img()
            ServerThread.server.send_to_motor(ConnectWindow.speed, ConnectWindow.motor_dir, False)
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
        self.conButton.clicked.connect(self.connect)
        self.leftButton.clicked.connect(self.set_left)
        self.rightButton.clicked.connect(self.set_right)
        self.quitButton.clicked.connect(self.quit)
        self.sendButton.clicked.connect(self.set_speed)

        self.statusText.setText("Status")
        self.portText.setPlaceholderText("Port")
        self.speedText.setPlaceholderText("Speed")

        self.speedText.setReadOnly(True)
        self.sendButton.setEnabled(False)
        self.leftButton.setEnabled(False)
        self.rightButton.setEnabled(False)
        self.quitButton.setEnabled(False)

        self.pixmap = None
        self.show()

    def set_img_view(self):
        frame = ServerThread.frame

        height, width, channel = frame.shape
        bytesPerLine = channel * width

        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(qImg)
        self.pixmap = self.pixmap.scaled(240, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imgLabel.setPixmap(self.pixmap)

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

        self.portText.setText("")
        self.statusText.setText("port : " + port)

        self.portText.setReadOnly(True)
        self.speedText.setReadOnly(False)

        self.conButton.setEnabled(False)
        self.sendButton.setEnabled(True)
        self.leftButton.setEnabled(True)
        self.rightButton.setEnabled(True)
        self.quitButton.setEnabled(True)

        self.th = ServerThread(port)
        self.th.print_signal.connect(self.set_img_view)
        self.th.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    connectWindow = ConnectWindow()
    connectWindow.show()
    app.exec_()
