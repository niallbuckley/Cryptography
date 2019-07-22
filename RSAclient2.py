import socket
from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP

def Main():
    MSG = "Client: OK"
    
    host = '127.0.0.1'
    port = 5000

    server = ('127.0.0.1',5000)

    #sock stream for TCP, DGRAM for udp
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind((host, port))
    s.connect((host, port))
    #s.sendto("Client: OK".encode('utf-8'), server)
    s.send(MSG.encode('utf-8'))
    print("ok!".encode('utf-8'))

    #Receive public key string from server
    server_string = s.recv(1024)

    #Remove extra characters
    #server_string = server_string.replace("public_key=", '')
    #server_string = server_string.replace("\r\n", '')

    #Convert string to key
    print("ok!! "+ str(server_string))
    server_public_key = RSA.importKey(server_string)
    print(server_public_key)
    print("ok!!!")

    message = input("-> ")
    while message != 'q':
        encryptor = PKCS1_OAEP.new(server_public_key)
        message = encryptor.encrypt(message.encode('utf-8'))
        #message = server_public_key.encrypt(message, 32)
        print("encrypted = " + str(message))
        s.sendto(message, server)
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print('Received from server: ' + data)
        if data == "Server stopped":
            break
        message = input("-> ")
    s.close()

if __name__ == '__main__':
    Main()
