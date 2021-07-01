from Crypto.Util.number import *
from secrets import *

T = 10
def encrypt(data):
    num = bytes_to_long(data)
    p = getPrime(512)
    q = getPrime(512)
    n = p*q
    assert num < n
    phi = (p-1)*(q-1)
    e = inverse(d,phi)
    a = pow(num,e,n)
    enc = long_to_bytes(a).encode('hex')
    return (n,e,enc)

flag = open('flag').read()
print d.bit_length()
for _ in xrange(T):
    data = flag + urandom(40)
    print encrypt(data)