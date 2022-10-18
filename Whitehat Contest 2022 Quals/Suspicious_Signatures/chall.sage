import os
from hashlib import sha256

# From https://neuromancer.sk/std/secg/secp256k1
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
K = GF(p)
a = K(0x0000000000000000000000000000000000000000000000000000000000000000)
b = K(0x0000000000000000000000000000000000000000000000000000000000000007)
E = EllipticCurve(K, (a, b))
G = E(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
E.set_order(n)

F = Zmod(n)

flag = os.urandom(32)
flag_hash = sha256(flag).hexdigest()
print(f"flag hash: {flag_hash}")
print(f"flag: FLAG{{{flag.hex()}}}")

d = int.from_bytes(flag, 'little')
assert d < n

msg = randint(1, n - 1)
k = randint(1, n - 1)
P = k * G
r = F(P.xy()[0])
s = F(msg + r * d) / F(k)
print(f'd= {d}')
print(f'k= {k}')
print(f"msg1= {msg}")
print(f"r1, s1= ({r}, {s})")

msg = randint(1, n - 1)
k = (k ** 3) % n
P = k * G
r = F(P.xy()[0])
s = F(msg + r * d) / F(k)

print(f"msg2 = {msg}")
print(f"r2, s2 = ({r}, {s})")

