import socket
from RSA import *

def encodeRSA(txt, open_exponent, n):
    txt = replacing_words(str(txt))
    res = fastpow(txt, open_exponent, module=n)
    return res


def decodeRSA(text, closed_exponent, n):
    res = fastpow(text, closed_exponent, module=n)
    return replacing_words(res)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
sock.connect(('', 9000))
print('Socket connected with server')
keys = RSA()
sock.send((keys.open_exponent).to_bytes(1024, 'big'))
sock.send((keys.n).to_bytes(1024, 'big'))
open_exp_s = int.from_bytes(sock.recv(1024), 'big')
n_s = int.from_bytes(sock.recv(1024), 'big')
print('Keys sent and received. Start sending messages')


data = ""


while True:
    input(data)
    if data == '~exit':
        exitmarker = 'User exited'
        exitmarker = encodeRSA(data, open_exp_s, n_s)
        sock.send(exitmarker.to_bytes(4096, 'big'))
        print('Exiting chat.')
        break
    data = encodeRSA(data, open_exp_s, n_s)
    sock.send(data.to_bytes(4096, 'big'))
    datar = int.from_bytes(sock.recv(4096), 'big')
    datar = decodeRSA(datar, keys.closed_exponent, keys.n)
    if datar == 'User exited':
        print('Another user exited. Closing chat')
    print(datar)


sock.close()
