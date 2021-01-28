from socket import *


class SocketConnection:
    ip = '192.168.1.8'
    port = 8485
    client = None
    
    def __init__(self):
        SocketConnection.client = socket(AF_INET, SOCK_STREAM)
        SocketConnection.client.connect((SocketConnection.ip, SocketConnection.port))
        print("Connected!")
            
    def send(self, data):
        SocketConnection.client.send(str(data).encode("utf-8"))
        
    def recv(self):
        data = SocketConnection.client.recv(1024)
        print(data.decode("utf-8"))
        return data.decode("utf-8")
        
    def close(self):
        SocketConnection.client.close()

if __name__ == '__main__':
    socket = SocketConnection()
    socket.send("Hello!")
    socket.recv()
    socket.close()
"""
ip = '192.168.1.8'
port = 8485

client = socket(AF_INET, SOCK_STREAM)
client.connect((ip, port))
print("Connected!")
    
client.send("Hello".encode("utf-8"))

client.close()
"""

