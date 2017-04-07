import socket
from tools_RSA import *
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
sock.bind(('', 9000))
print('Socket binded')
sock.listen(2)
print('Socket listening')
conn_f, addr_f = sock.accept()
print('Connected with' + addr_f[0] + ':' + str(addr_f[1]))
oef = int.from_bytes(sock.recv(1024), 'big')
ncl_f = int.from_bytes(sock.recv(1024), 'big')
keysf = RSA()
conn_f.send((keysf.open_exponent).to_bytes(1024, 'big'))  # client gets info to decode messages from server
conn_f.send((keysf.n).to_bytes(1024, 'big'))
conn_s, addr_s = sock.accept()
print('Connected with' + addr_s[0] + ':' + str(addr_s[1]))
oes = int.from_bytes(sock.recv(1024), 'big')
ncl_s = int.from_bytes(sock.recv(1024), 'big')
keyss = RSA()
conn_f.send((keyss.open_exponent).to_bytes(1024, 'big'))  # client gets info to decode messages from server
conn_f.send((keyss.n).to_bytes(1024, 'big'))
print('Both users are connected')
'''
while True:
    data = conn_f.recv(1024)
    dataS = conn_s.recv(1024)
    if not data and dataS:
        break
    data = encodeRSA(oef, data, ncl_f)
    data = decodeRSA(data, cls, ncl_s)
    dataS = encodeRSA(oes, dataS, ncl_s)
    dataS = decodeRSA(dataS, clf, ncl_f)
    user_f.send(dataS)
    user_s.send(data)
sock.close()
print('Socket closed')
'''