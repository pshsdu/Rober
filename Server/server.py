from socket import *
import cv2
import numpy as np


class Server:
    host = ''  # allow connection from any ip
    port = 0

    window_name = 'Camera 1'
    socket = None
    conn = None

    def __init__(self, port):
        Server.port = port
        Server.__init_server()

    # ------------------------------------------------
    # Making new listening server
    # ------------------------------------------------
    @staticmethod
    def __init_server():
        # Making new socket
        Server.socket = socket(AF_INET, SOCK_STREAM)

        Server.socket.bind((Server.host, Server.port))
        Server.socket.listen(10)

        print('Socket is initialized')

        # Waiting for client to come
        Server.conn, addr = Server.socket.accept()
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
        Server.conn.send(output.encode("utf-8"))

    # ------------------------------------------------
    # Get image from input numpy array about camera
    # ------------------------------------------------
    def get_img(self):
        length = Server.recvall(Server.conn, 16)
        stringData = Server.recvall(Server.conn, int(length))

        data = np.fromstring(stringData, dtype='uint8')
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
        frame = self.get_img()

        cv2.imshow(self.window_name, frame)

    def close(self):
        Server.socket.close()
        cv2.destroyAllWindows()
        exit(0)


if __name__ == "__main__":
    server = Server(8485)

    while True:
        try:
            server.send_to_motor(350, 'r', False)
            server.stream_camera()

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

        except KeyboardInterrupt:
            server.close()
            break

    exit(0)
