import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP
import ast


def Main():
    enc = False
    #Generate private and public keys
    random_generator = Random.new().read
    private_key = RSA.generate(1024, random_generator)
    public_key = private_key.publickey()
    
    host = '127.0.0.1'
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)

    data = ""
    c, addr = s.accept() 

    print("Server Started.")

    while True:
        data = c.recv(1024)
        if enc:
            print ("Received:\nEncrypted message = "+str(data))
            decryptor = PKCS1_OAEP.new(private_key)
            data = decryptor.decrypt(ast.literal_eval(str(data)))
            print ("Decrypted message = " + str(data))

        #Wait until data is received.
        data = data.decode('utf-8')
        data = data.replace("\r\n", '') #remove new line character

        if data == "Client: OK":
            print(public_key.exportKey())
            c.send(public_key.exportKey())
            #s.sendall(public_key.exportKey())
            print("Public key sent to client.")
            enc = True

        elif data == "Nein!": break

        else:
            c.send(b"Server: OK")

    c.send(b"Server stopped")
    print ("Server stopped")
    s.close()

if __name__ == '__main__':
    Main()

