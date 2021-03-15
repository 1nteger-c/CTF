import base64
from pwn import *
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
r = remote('crypto.ctf.zer0pts.com', 10130)

r.recvuntil('Encrypted flag: ')
c = r.recvline()[:-1]
c = base64.b64decode(c)
iv = c[:16]
print(iv)
cipher = c[16:]
print(cipher)
r.recvuntil('p = ')
p = int(r.recvline()[:-1])
print(p)
r.recvline()
key = ''
for i in range(32*4):
    r.recvuntil('t = ')
    t = int(r.recvline()[:-1])

    a = 3
    b = 27
    d = 9
    c = t

    #print(a, b, c, d)

    r.sendlineafter(b'a = ', str(a))
    r.sendlineafter(b'b = ', str(b))
    r.sendlineafter(b'c = ', str(c))
    r.sendlineafter(b'd = ', str(d))

    x = int(r.recvline()[4:])
    y = int(r.recvline()[4:])
    z = int(r.recvline()[4:])
    #print(x, y, z)
    if ((x * y) % p) == ((z ** 2) % p):
        key = '00' + key
    elif (((x ^ 1) * y) % p) == ((z ** 2) % p):
        key = '01' + key
    elif ((x * (y ^ 1)) % p) == ((z ** 2) % p):
        key = '10' + key
    elif (((x ^ 1) * (y ^ 1)) % p) == ((z ** 2) % p):
        key = '11' + key
    else:
        print('error')
    print(key)
key = int(key, 2)
key = long_to_bytes(key)
aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
p = unpad(aes.decrypt(cipher), 16)
print('flag is : ', p)
r.interactive()
