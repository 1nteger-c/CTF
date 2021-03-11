from pwn import *
from gmpy2 import jacobi
while(1):
    r = remote('crypto.ctf.zer0pts.com', 10463)
    r.recvuntil('g: ')
    g = int(r.recvuntil(',')[:-1])
    r.recvuntil('p: ')
    p = int(r.recvline()[:-1])

    li = [jacobi(1, p), jacobi(2, p), jacobi(3, p)]
    val = 0
    win = 0
    if li != [1, -1, -1] or jacobi(g, p) != 1:
        print("ERROR")
        continue

    else:
        while(1):
            r.recvuntil(' my commitment is=(')
            a = int(r.recvuntil(',')[:-1])
            b = int(r.recvuntil(')')[:-1])
            a1 = jacobi(a, p)
            b1 = jacobi(b, p)
            if a1 == b1:

                r.sendline('3')
            else:
                r.sendline('2')
            r.recvline()
            r.recvline()
            r.recvline()
            r.recvline()
            get = (r.recvline())
            if b'win' in get:
                win += 1
                print('score : ', win)
                if win == 100:
                    break
        r.interactive()
