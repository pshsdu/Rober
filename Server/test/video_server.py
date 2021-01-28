from socket import *
import cv2
import numpy as np


class Server:
    def __init__(self, port, window_name, cam_num):
        self.host = ''
        self.window_name = window_name
        self.port = port
        self.socket = None
        self.conn = None
        self.cam_num = cam_num

        self.init_server()
        # self.connect()

    def init_server(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print('Socket is initialized')

        self.conn, addr = self.socket.accept()
        print('Connected!')

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def get_img(self):
        length = self.recvall(self.conn, 16)
        stringData = self.recvall(self.conn, int(length))

        data = np.fromstring(stringData, dtype='uint8')
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame

    def get_data(self):
        length = self.recvall(self.conn, 16)

        if length is not None:
            stringData = self.recvall(self.conn, int(length))
            data = np.fromstring(stringData, dtype='uint8')
            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        else:
            return None

    def stream(self):
        images = list()

        for i in range(0, self.cam_num):
            frame = self.get_img()

            cv2.imshow(self.window_name[i], frame)


if __name__ == '__main__':
    names = ['camera 1', 'camera 2', 'camera 3']
    server1 = Server(8485, names, 3)
    # server2 = Server(8486, 'Camera 1')

    while True:
        server1.stream()
        # server2.stream()
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    server1.socket.close()
    # server2.socket.close()
    cv2.destroyAllWindows()
    exit(0)

    # server1 = Server(8486, 'Camera 2')
