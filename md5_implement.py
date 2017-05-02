import math

rotation = lambda info, am: ((info << am) | (info >> (32 - am)))

rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                  5, 9, 14, 20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15,
                  21, 6, 10, 15, 21, 6, 10, 15, 21]

sValue = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

funcOne = 16 * [lambda x, y, z: (x & y) | (~x & z)] + \
            16 * [lambda x, y, z: (x & z) | (~z & y)] + \
            16 * [lambda x, y, z: x ^ y ^ z] + \
            16 * [lambda x, y, z: y ^ (~z | x)]

funcTwo = 16 * [lambda l: l] + \
                  16 * [lambda l: (5 * l + 1) % 16] + \
                  16 * [lambda l: (3 * l + 5) % 16] + \
                  16 * [lambda l: (7 * l) % 16]

constants = [int(abs(math.sin(i + 1)) * 2 ** 32) for i in range(64)]

message = input().encode('ascii')
mess = bytearray(message)
oLen = (8 * len(mess))
mess.append(0x80)
while len(mess) % 64 != 56:
    mess.append(0)
mess += oLen.to_bytes(8, byteorder='little')
pieces = sValue
for numberR in range(0, len(mess), 64):
    a, b, c, d = pieces
    chunk = mess[numberR:numberR + 64]
    for i in range(64):
        f = funcOne[i](b, c, d)
        print(f)
        g = funcTwo[i](i)
        infToRot = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
        new_b = (b + rotation(infToRot, rotate_amounts[i])) & 0xFFFFFFFF
        a, b, c, d = d, new_b, b, c
    for i, val in enumerate([a, b, c, d]):
        pieces[i] += val
        pieces[i] &= 0xFFFFFFFF
result = sum(x << (32 * i) for i, x in enumerate(pieces))
result = result.to_bytes(16, byteorder = 'little')
result = '{:032x}'.format(int.from_bytes(result, byteorder='big'))
print(result)
