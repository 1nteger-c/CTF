from Crypto.Util.number import *
from hashlib import md5
from Crypto.Cipher import AES
import pickle
f = open('a.txt', 'rb')
c = pickle.load(f)


s = '3eb0f38f3d128b7889adcbcab185573857d373e764704280418131c4dbfbb22b'
flag = 'e622fc6690a7efc8ebe0f14a33d4130f:035e94920ec1c9e2fc53fa600a1cc7f8:33eb533eff1ed6ec6f56702365392d2bc627ed023fd94f9644fe92069da480f252c3e399e10494bc2070653bcb91095f'

p1 = long_to_bytes(int(s[:32], 16))
p2 = long_to_bytes(int(s[32:], 16))
iv1 = '\x00' * 16
iv2 = b'\x00' * 16
keys_list = []
start = 3 * 2 ** 22
for i in range(start, start + 2 ** 22):
    if i % (2 ** 20) == 0:
        print(hex(i))
    key = md5(long_to_bytes(i)).digest()
    cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv2, segment_size=8*16)
    k = bytes_to_long(cipher.encrypt(iv2))
    s = 0
    f = 2**24-1
    while(s <= f):
        mid = (s + f) // 2
        if c[mid][1] < k:
            s = mid+1
        elif c[mid][1] > k:
            f = mid - 1
        else:
            print('get !!')
            print("key0 : ", c[mid][0])
            print("key2 : ", i + start)
            keys_list.append((c[mid][0], i+start))
            break
print(keys_list)
