load("small_roots.sage")

import random
from pwn import *
p = 8088430881271757130274784339253665338335626861355585318498924098872329526068810418778223672826275708502108494947472904429048917317830146855112324148596307
q = 8000610987505880224296183684383189690409761101334714895423889508209590519034875705962809615495410114999121400419438307185857949951398310688366322313090379
e = 43141592653589793238462643383279502884197169399375105820974944592307816406286012029957257665311892599272760841354029508833862170149297061469463995174000179889100502245620696926992798286112311731694241066719524989045789851259929870964395693863447149033024524160971530391030421457888460231006282766051743295779
n = p * q

r = process(['python3','chal.py'])

r.sendline(str(p))
r.sendline(str(q))
r.sendline(str(e))
r.recvuntil(b'First Outputs\n')
next_out = int(r.recvline())

def inc_state(state):
    next_z = pow(state, e, n)
    next_out = int(next_z) % (1 << 896)
    next_state = next_z >> 896 
    return next_out, next_state

def recover_state1(next_out):
    # known : next_out
    # (a * 2^896 + next_out) ** 3 - b = 0 (mod n)
    # a, b : 128 bit
    # 1. Using defund's multivariate coppersmith 
    # https://github.com/defund/coppersmith/blob/master/coppersmith.sage
    
    Pr.<a,b> = PolynomialRing(Zmod(n))
    f = (a * 2^896 + next_out) **3 - b
    res = small_roots(f, (2 ^ 128, 2 ^ 128))
    a, b = res[0]
    assert ((a * 2^896 + next_out) ** 3 - b) % n == 0
    return a

state = recover_state1(next_out)
next_out, state = inc_state(state)
r.sendline(str(next_out))
r.sendline(str(state))
r.interactive()
