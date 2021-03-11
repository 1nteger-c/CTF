from Crypto.Util.number import *
from hashlib import md5
from Crypto.Cipher import AES
import pickle


s = '3eb0f38f3d128b7889adcbcab185573857d373e764704280418131c4dbfbb22b'
flag = 'e622fc6690a7efc8ebe0f14a33d4130f:035e94920ec1c9e2fc53fa600a1cc7f8:33eb533eff1ed6ec6f56702365392d2bc627ed023fd94f9644fe92069da480f252c3e399e10494bc2070653bcb91095f'
key0 = 7503913
key2 = 2593811
key1 = 0
key0 = md5(long_to_bytes(key0)).digest()
key2 = md5(long_to_bytes(key2)).digest()
iv1 = b'\x00' * 16
iv2 = b'\x00' * 16
c = b'\x00' * 32
p = long_to_bytes(
    0x3eb0f38f3d128b7889adcbcab185573857d373e764704280418131c4dbfbb22b)
c0 = AES.new(key0, mode=AES.MODE_ECB)
c2 = AES.new(key2, mode=AES.MODE_CFB, iv=iv2, segment_size=8*16)
p = c0.encrypt(p)
c = c2.decrypt(c)
for i in range(0, , 2**24):
    if i % (2 ** 19) == 0:
        print(hex(i))
    c1 = AES.new(md5(long_to_bytes(i)).digest(), mode=AES.MODE_CBC, iv=iv1)

    if c1.encrypt(p) == c:
        print('get !! : ', i)
        key1 = i
        break

key1 = 4176040
c1 = AES.new(md5(long_to_bytes(key1)).digest(), mode=AES.MODE_CBC, iv=iv1)
iv1 = long_to_bytes(0xe622fc6690a7efc8ebe0f14a33d4130f)
iv2 = long_to_bytes(0x035e94920ec1c9e2fc53fa600a1cc7f8)
c = long_to_bytes(
    0x33eb533eff1ed6ec6f56702365392d2bc627ed023fd94f9644fe92069da480f252c3e399e10494bc2070653bcb91095f)
c1 = AES.new(md5(long_to_bytes(key1)).digest(), mode=AES.MODE_CBC, iv=iv1)
c0 = AES.new(key0, mode=AES.MODE_ECB)
c2 = AES.new(key2, mode=AES.MODE_CFB, iv=iv2, segment_size=8*16)
cipher = [c0, c1, c2]
for i in range(3):
    c = cipher[2-i].decrypt(c)
print(c)
