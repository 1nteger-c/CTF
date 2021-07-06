from pwn import *
from Crypto.Util.number import *
from Crypto.Util.strxor import strxor
r = process(['python3','server.py'])

r.recvuntil('sh and its signature ')
sig = bytes.fromhex(r.recvline()[:-2].decode())
print(len(sig))
enc = sig[:16]
iv = sig[16:]

iv = strxor(iv,b'flagflagflagflag')
iv = strxor(iv,b'cashcashcashcash')
r.recvuntil(': ')
r.sendline(str('flag'*4))
r.sendline(enc.hex() + iv.hex())
r.interactive()