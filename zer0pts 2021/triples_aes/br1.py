from Crypto.Cipher import AES
from hashlib import md5
from Crypto.Util.number import *
import pickle
s = '3eb0f38f3d128b7889adcbcab185573857d373e764704280418131c4dbfbb22b'
flag = 'e622fc6690a7efc8ebe0f14a33d4130f:035e94920ec1c9e2fc53fa600a1cc7f8:33eb533eff1ed6ec6f56702365392d2bc627ed023fd94f9644fe92069da480f252c3e399e10494bc2070653bcb91095f'
p1 = long_to_bytes(int(s[:32], 16))
p2 = long_to_bytes(int(s[32:], 16))
iv1 = '00' * 16
iv2 = '00' * 16
save = {}

for i in range(0, 2 ** 24):
    if i % (2 ** 20) == 0:
        print(hex(i))
    key = md5(long_to_bytes(i)).digest()
    cipher = AES.new(key, mode=AES.MODE_ECB)
    k = bytes_to_long(cipher.encrypt(p1)) ^ bytes_to_long(cipher.encrypt(p2))
    save[i] = k
save = sorted(save.items(), key=lambda x: x[1])
f = open("a.txt", "wb")
pickle.dump(save, f)
f.close()
