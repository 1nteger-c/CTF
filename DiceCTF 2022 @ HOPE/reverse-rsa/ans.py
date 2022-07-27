from pwn import *
from Crypto.Util.number import *
r = remote('mc.ax',31669)

flag_regex = rb"hope{[a-zA-Z0-9_\-]+}"

with open("ciphertext.txt", "r") as f:
	c = int(f.read(), 10)


r.recvuntil(b'Welcome to reverse RSA! The encrypted flag is ')
c = int(r.recvuntil(b'.')[:-1])
## use https://www.alpertron.com.ar/DILOG.HTM
p = 15800822948503579453
q = 3
d = 4394449733029816003
N = p*q

m = pow(c,d,p*q)
phi = (p-1) * (q-1)
e = inverse(d,phi)
r.sendlineafter(b': ',str(p))
r.sendlineafter(b': ',str(q))
r.sendlineafter(b': ',str(e))

r.interactive()
