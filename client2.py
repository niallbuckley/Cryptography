import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def Main():
##    private_key = rsa.generate_private_key(
##        public_exponent=65537,
##        key_size=2048,
##        backend=default_backend()
##    )
##    public_key = private_key.public_key()
    
    host = '192.168.1.20'
    port = 5044

    server = ('192.168.1.20',5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    message = input("-> ")
    while message != 'q':
##        ciphertext = public_key.encrypt(
##            message,
##            padding.OAEP(
##            mgf=padding.MGF1(algorithm=hashes.SHA256()),
##            algorithm=hashes.SHA256(),
##            label=None
##            )
##        )
        print(message)
        s.sendto(message.encode('utf-8'), server)
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print('Received from server: ' + data)
        message = input("-> ")
    s.close()

if __name__ == '__main__':
    Main()
