import socket
from RSA import *

def encodeRSA(open_exponent, txt, n):
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
print('Keys sent and received. Start sending data')
data = ""
while True:
    input(data)
    dataR = sock.recv(1024)
    if not data and dataR:
        break
    data =  decodeRSA(data, keys.closed_exponent, keys.n)
    dataR = encodeRSA(open_exp_s, dataR, n_s)
    print(dataR)
sock.close()
print('Socket closed')