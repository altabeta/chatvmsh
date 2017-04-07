import socket
from tools_RSA import *
from RSA import *


def encodeRSA(txt, open_exponent, n):
    txt = replacing_words(str(txt))
    res = fastpow(txt, open_exponent, module=n)
    return res


def decodeRSA(text, closed_exponent, n):
    res = fastpow(text, closed_exponent, module=n)
    return replacing_words(res)

# Creating a listening socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
sock.bind(('', 9000))
print('Socket binded')
sock.listen(2)
print('Socket listening')

# Receiving first connection, creating RSA keys for sending, receiving keys to decode (client 1)

conn_f, addr_f = sock.accept()
print('Connected with' + addr_f[0] + ':' + str(addr_f[1]))
oef = int.from_bytes(conn_f.recv(1024), 'big')
nf = int.from_bytes(conn_f.recv(1024), 'big')  # receiving keys from client
keysf = RSA()
conn_f.send((keysf.open_exponent).to_bytes(1024, 'big'))  # sending keys to client
conn_f.send((keysf.n).to_bytes(1024, 'big'))
print('User 1 connected, keys sent and received')

# Receiving first connection, creating RSA keys for sending, receiving keys to decode (client 2)

conn_s, addr_s = sock.accept()
print('Connected with' + addr_s[0] + ':' + str(addr_s[1]))
oes = int.from_bytes(conn_s.recv(1024), 'big')
ns = int.from_bytes(conn_s.recv(1024), 'big') # receiving keys from client
keyss = RSA()
conn_s.send((keyss.open_exponent).to_bytes(1024, 'big'))  # sending keys to client
conn_s.send((keyss.n).to_bytes(1024, 'big'))
print('User 2 connected, keys sent and received')

# Start of info exchange

while True:
    data = int.from_bytes(conn_f.recv(4096), 'big')
    datas = int.from_bytes(conn_s.recv(4096), 'big')
    if not data and datas:
        break
    data = decodeRSA(data, keysf.closed_exponent, keysf.n)
    datas = decodeRSA(datas, keyss.closed_exponent, keyss.n)
    data = encodeRSA(datas, oef, nf)
    datas = encodeRSA(data, oes, ns)
    conn_f.send((data).to_bytes(4096, 'big'))
    conn_s.send((datas).to_bytes(4096, 'big'))
sock.close()
print('Socket closed')
