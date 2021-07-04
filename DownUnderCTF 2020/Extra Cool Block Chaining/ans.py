from pwn import *
from Crypto.Util.number import *
from Crypto.Util.strxor import strxor
flag = b''
block = []
#flag[0]
r = process(['python3','server.py'])
r.recvuntil(': ')
cipher = r.recvline()[:-1]
cipher = bytes.fromhex(cipher.decode())
r.recvuntil(': ')
r.sendline('10'*16)
r.recvuntil(': ')
r.sendline(cipher[:16].hex())
flag += bytes.fromhex(r.recvline()[:-1].decode())
print(flag)
r.close()
# DUCTF{4dD1nG_r4n 

#flag[2:]
for i in range(2,6):
    r = process(['python3','server.py'])
    r.recvuntil(': ')
    cipher = r.recvline()[:-1]
    cipher = bytes.fromhex(cipher.decode())
    r.recvuntil(': ')
    r.sendline('10'*16)
    iv = bytes.fromhex(r.recvline().decode())[16:]
    r.recvuntil(': ')
    tmp1 = strxor(cipher[(i-1)*16:(i)*16] , cipher[(i) * 16 : (i+1) * 16])
    tmp2 = strxor(tmp1 , iv)
    r.sendline(tmp2.hex())
    flag += bytes.fromhex(r.recvline()[:-1].decode())
    print(flag)
    r.close()

#DUCTF{4dD1nG_r4n0RS_h3r3_4nD_th3R3_U5u4Lly_H3lps_Bu7_n0T_7H1s_t1m3_i7_s33ms!!}