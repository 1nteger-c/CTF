import os

n = int.from_bytes(os.urandom(4096 // 8), 'big')
n |= 1 << 4096

def f(x, y):
    t, r = x, 0
    while y:
        if y & 1:
            r ^= t
        y >>= 1
        t <<= 1
        if t >> 4096:
            t ^= n
    return r

def g(x, y):
    t, r = x, 1
    while y:
        if y & 1:
            r = f(r, t)
        y >>= 1
        t = f(t, t)
    return r

flag = b"DH{example_flag}"
flag += os.urandom(4096 // 8 - len(flag) - 1)

flag = int.from_bytes(flag, 'big')
c = g(flag, 0x10001)

print("n =", hex(n))
print("c =", hex(c))