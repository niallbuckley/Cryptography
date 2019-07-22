import socket
import threading
import sys

class Server:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = ""
    connections = []
    host = '127.0.0.1'
    port = 5000
    
    def __init__(self):
        self.s.bind((self.host,self.port))
        self.s.listen(5)

    def run(self):
        while True:
            c, addr = self.s.accept()
            #create a thread as it is necessary for multiple clients to be able to connect
            currentT = threading.Thread(target = self.handler, args = (c, addr))
            currentT.daemon = True
            currentT.start()
            self.connections.append(c)
            print(self.connections)

    def handler(self, c, addr):
        while True:
            data = c.recv(1024)
            for clients in self.connections:
                clients.send(data)
            if not data:
                break

class Client:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5000
    def sendMsg(self):
        self.s.send(bytes(input("-> "), 'utf-8'))
        #s.sendto(message, server)
        
    def __init__(self, addr):
        self.s.connect((addr, self.port))
        #need a thread as we can't recieve and send data at the same time
        currentT = threading.Thread(target = self.sendMsg)
        currentT.daemon = True
        currentT.start()
        
        while True:
            data, addr = self.s.recvfrom(1024)
            data = data.decode('utf-8')
            print('Received from server: ' + data)
            if not data:
                break
            

if (len(sys.argv)>1):
    client = Client(sys.argv[1])

else:
    server = Server()
    server.run()
