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
sock.bind(('', 9290))
print('Socket binded')
sock.listen(2)
print('Socket listening')

# Receiving first connection, creating RSA keys for sending, receiving keys to decode (client 1)

conn_f, addr_f = sock.accept()
print('Connected with' + addr_f[0] + ':' + str(addr_f[1]))
oef = int(conn_f.recv(4096))
nf = int(conn_f.recv(4096))  # receiving keys from client
print('oef_' + str(oef))
print('nf_' + str(nf))
keysf = RSA()
conn_f.send(str(keysf.open_exponent).encode('utf-8'))  # sending keys to client
conn_f.send(str(keysf.n).encode('utf-8'))
print('User 1 connected, keys sent and received')

# Receiving first connection, creating RSA keys for sending, receiving keys to decode (client 2)

conn_s, addr_s = sock.accept()
print('Connected with' + addr_s[0] + ':' + str(addr_s[1]))
oes = int(conn_s.recv(4096))
ns = int(conn_s.recv(4096)) # receiving keys from client
print('oes_' + str(oes))
print('ns_' + str(ns))
keyss = RSA()
conn_s.send(str(keyss.open_exponent).encode('utf-8'))  # sending keys to client
conn_s.send(str(keyss.n).encode('utf-8'))
print('User 2 connected, keys sent and received')

# Start of info exchange

while True:
    print('Start of cycle')
    data = int(conn_f.recv(4096))
    print('Msg 1 before decoding' + ' ' + str(data))
    data = decodeRSA(data, keysf.closed_exponent, keysf.n)
    print('Recieved first message:' + ' ' + str(data))
    if data == 'User exited':
        print('1st data unreachable')
        break
    datas = int(conn_s.recv(4096))
    print('Msg 2 before decoding' + ' ' + str(data))
    datas = decodeRSA(datas, keyss.closed_exponent, keyss.n)
    print('Recieved second message:' + ' ' + str(datas))
    if datas == 'User exited':
        print('2nd data unreachable')
        break
    datatf = encodeRSA(datas, oef, nf)
    datats = encodeRSA(data, oes, ns)
    conn_f.send(str(datatf).encode('utf-8'))
    conn_s.send(str(datats).encode('utf-8'))
    print('Data sent')
sock.close()
print('Socket closed')
