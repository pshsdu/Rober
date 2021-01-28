from socket import *
import cv2
import numpy as np


class Server:

    def __init__(self, port, cam_num):
        self.host = ''
        self.port = port
        # self.window_name = window_name
        self.socket = None
        self.conn = None
        self.cam_num = cam_num
        self.__init_server()

    # ------------------------------------------------
    # Making new listening server
    # ------------------------------------------------
    def __init_server(self):
        # Making new socket
        self.socket = socket(AF_INET, SOCK_STREAM)

        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print('Socket is initialized')

        # Waiting for client to come
        self.conn, addr = self.socket.accept()
        print('Connected!')

    # ------------------------------------------------
    # Repeat by input data length
    # Add input data to buffer
    # ------------------------------------------------
    @staticmethod
    def recvall(sock, count):
        buf = b''  # byte object
        while count:
            new_buf = sock.recv(count)
            if not new_buf:
                return None
            buf += new_buf
            count -= len(new_buf)
        return buf

    # ------------------------------------------------
    # Send speed, direction information to motor drive
    # ------------------------------------------------
    def send_to_motor(self, speed, direction, is_quit):
        if is_quit:
            self.close()

        # Saturate the speed of motor, max motor speed = 1000rpm
        if speed >= 1000:
            speed = 1000
        elif speed <= 0:
            speed = 0

        # data form : % speed / direction %
        if direction == 'r':
            output = "%" + str(speed) + "/" + str(1) + "%"
        elif direction == 'l':
            output = "%" + str(speed) + "/" + str(0) + "%"
        else:
            print("invalid input")

        # data sending, encoding type = utf-8
        self.conn.send(output.encode("utf-8"))

    # ------------------------------------------------
    # Get image from input numpy array about camera
    # ------------------------------------------------
    def get_img(self):
        length = Server.recvall(self.conn, 16)
        stringData = Server.recvall(self.conn, int(length))

        data = np.fromstring(stringData, dtype='uint8')
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame

    # test function
    def input(self):
        try:
            print("----------------------------------")
            data = input("speed (integer): ")
            direction = raw_input("direction (r/l): ")
            self.send_to_motor(data, direction, False)

        except EOFError:
            print("Quit")
            self.send_to_motor(None, None, True)

    # test function
    def stream_camera(self):
        images = list()

        for i in range(0, self.cam_num):
            images.append(self.get_img())

        return images

    def close(self):
        self.socket.close()
        cv2.destroyAllWindows()
        exit(0)


if __name__ == "__main__":
    names = ['camera 1', 'camera 2', 'camera 3']
    server1 = Server(8485, names, 3)

    while True:
        try:
            server1.send_to_motor(350, 'r', False)
            server1.stream_camera()

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

        except KeyboardInterrupt:
            server1.close()
            break

    exit(0)
