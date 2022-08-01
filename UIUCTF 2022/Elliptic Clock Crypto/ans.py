
from hashlib import md5
from Crypto.Cipher import AES
from sage.all import *
# 256-bit security!
p = 62471552838526783778491264313097878073079117790686615043492079411583156507853

class Fp:
    def __init__(self,x):
        self.int = x % p
    def __str__(self):
        return str(self.int)
    __repr__ = __str__
    def __int__(self):
        return self.int
    def __eq__(a,b):
        return a.int == b.int
    def __ne__(a,b):
        return a.int != b.int
    def __add__(a,b):
        return Fp(a.int + b.int)
    def __sub__(a,b):
        return Fp(a.int - b.int)
    def __mul__(a,b):
        return Fp(a.int * b.int)
    def __truediv__(a,b):
        return a*Fp(pow(b.int,-1,p))

class ClockPoint:
    def __init__(self,x,y):
        assert int(x*x + y*y) == 1
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x},{self.y})"
    def __eq__(self, other):
        return str(self) == str(other)
    __repr__ = __str__
    def get_hash(self):
        return md5(str(self).encode()).digest()
    def __add__(self, other):
        x1,y1 = self.x, self.y
        x2,y2 = other.x, other.y
        return ClockPoint( x1*y2+y1*x2, y1*y2-x1*x2 )

def scalar_mult(x: ClockPoint, n: int) -> ClockPoint:
    y = ClockPoint(Fp(0),Fp(1))
    if n == 0: return y
    if n == 1: return x
    while n > 1:
        if n % 2 == 0:
            x = x + x
            n = n // 2
        else:
            y = x + y
            x = x + x
            n = (n-1) // 2
    return x + y


base_point = ClockPoint(Fp(34510208759284660042264570994647050969649037508662054358547659196695638877343),Fp(4603880836195915415499609181813839155074976164846557299963454168096659979337))
with open("output.txt",'r') as f:
    alice = eval(f.readline().split(':')[1])
    bob = eval(f.readline().split(':')[1])
    enc = eval(f.readline().split(':')[1])
## find i^2 == -1 mod p
F = IntegerModRing(p)
i = F(-1).sqrt()
print(i)

base = (int(base_point.x) * i + int(base_point.y)) % p

alice = (alice[0] * i + alice[1]) % p
bob = (bob[0] * i + bob[1]) % p

alice_secret = discrete_log(F(alice), F(base))
bob_secret = discrete_log(F(bob), F(base))

shared_secret = scalar_mult(base_point, bob_secret * alice_secret)
key = shared_secret.get_hash()

print(b"Encrypted flag: ", AES.new(key, AES.MODE_ECB).decrypt(enc))
#uiuctf{Circle5_ar3_n0t_ell1ptic}