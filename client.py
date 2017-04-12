import socket
from RSA import *

def encodeRSA(txt, open_exponent, n):
    print(txt)
    txt = replacing_words(str(txt))
    res = fastpow(txt, open_exponent, module=n)
    return res


def decodeRSA(text, closed_exponent, n):
    res = fastpow(text, closed_exponent, module=n)
    return replacing_words(res)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
sock.connect(('', 9290))
print('Socket connected with server')
keys = RSA()
print('oe' + str(keys.open_exponent))
print('n' + str(keys.n))
sock.send(str((keys.open_exponent)).encode('utf-8'))
sock.send((str(keys.n)).encode('utf-8'))
open_exp_s = int(sock.recv(4096))
n_s = int(sock.recv(4096))
print('Keys sent and received. Start sending messages')

data = ""

while True:
    data = input()
    if data == 'exi':
        exitmarker = 'User exited'
        exitmarker = encodeRSA(data, open_exp_s, n_s)
        sock.send(str(exitmarker).encode('utf-8'))
        print('Exiting chat.')
        break
    data = encodeRSA(data, open_exp_s, n_s)
    sock.send(str(data).encode('utf-8'))
    datar = int(sock.recv(4096))
    datar = decodeRSA(datar, keys.closed_exponent, keys.n)
    if datar == 'User exited':
        print('Another user exited. Closing chat')
    print(datar)


sock.close()