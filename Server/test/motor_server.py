from socket import *
import keyboard

class Server:
    HOST = ''
    PORT = 0

    INIT_SPEED = 200
    INIT_DIR = 0

    socket = None
    conn = None
    
    def __init__(self, port):
        Server.PORT = port
        self.init_server()

    def init_server(self):
        Server.socket = socket(AF_INET, SOCK_STREAM)

        Server.socket.bind((Server.HOST, Server.PORT))
        Server.socket.listen(10)

        Server.conn, addr = Server.socket.accept()
        print('Connected!')
        print('Ctrl+D : Quit')

        data = Server.INIT_SPEED
        direction = Server.INIT_DIR

    def input(slef):
        try:
            print("----------------------------------")
            data = input("speed (integer): ")
            direction = raw_input("direction (r/l): ")
            send(data, direction, False)
        except EOFError:
            print("Quit")
            send(None, None, True)
        
    def send(self, speed, direction, is_quit):
  
        # while True:
        # try:
        #     print("----------------------------------")
        #     data = input("speed (integer): ")
        #     direction = raw_input("direction (r/l): ")
        # except EOFError:
        #     print("Quit")

        if is_quit:
            self.close()

        if speed >= 1000:
            speed = 1000
        elif speed <= 0:
            speed = 0

        if direction == 'r':
            output = str(data) + "," + str(1)
        elif direction == 'l':
            output = str(data) + "," + str(0)
        else:
            print("invalid input")
        
        Server.conn.send(output.encode("utf-8"))
        print(output)

        # Server.conn.close()
        # Server.socket.close()

    def close(self):
        Server.conn.close()
        Server.socket.close()
        exit(0)

if __name__ == "__main__":
    server = Server(8486)

    while True:
        server.input()


    