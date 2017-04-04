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


def user_setup():
    conn, addr = sock.accept()
    print('Connected with' + addr[0] + ':' + str(addr[1]))
    open_exponent = int(conn.recv(1024))
    n = int(conn.recv(1024))
    keys = RSA()
    conn.send(keys.open_exponent)  # client gets info to decode messages from server
    conn.send(keys.n)
    return open_exponent, n, keys.closed_exponent, keys.n, conn


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
sock.bind(('', 9000))
print('Socket binded')
sock.listen(2)
print('Socket listening')
oef, nf, clf, ncl_f, user_f = user_setup()
oes, ns, cls, ncl_s, user_s = user_setup()
while True:
    data = user_f.recv(1024)
    dataS = user_s.recv(1024)
    if not data and dataS:
        break
    data = encodeRSA(oef, data, nf)
    data = decodeRSA(data, cls, ncl_s)
    dataS = encodeRSA(oes, dataS, ns)
    dataS = decodeRSA(dataS, clf, ncl_f)
    user_f.send(dataS)
    user_s.send(data)
sock.close()