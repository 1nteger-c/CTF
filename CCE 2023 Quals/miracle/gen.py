from Crypto.Util.number import *
import random
# make p, q, e ## 3e = 2(p-1)(q-1) + 1

ee = 3141592653589793238462643383279502884197169399375105820974944592307816406286
nn = 2718281828459045235360287471352662497757247093699959574966967627724076630353
ee = int('4' + str(ee)) # to match q as 512bit.
e = random.randrange(2 ** 1022, 2 ** 1024)
ee_min = ee
ee_max = ee
while(True):
    if ee_min.bit_length() >= 1022:
        break
    ee_min = ee_min * 10
    ee_max = ee_min + 9

mask = 10 ** 76
while(True):
    p = getPrime(512)
    e = random.randrange(ee_min, ee_max)
    tmp = 3 * e - 1
    q = tmp // (2 * (p-1))
    
    last = inverse(p, mask) * nn
    q = (q // mask) * mask + last % mask
    if not isPrime(q):
        continue
    print(q.bit_length())
    if q.bit_length() != 512:
        continue
    n = p * q
    if str(nn) not in str(n):
        continue
    
    _3e = 2 * (p-1) * (q-1) + 1
    if _3e % 3:
        continue
    e = _3e // 3

    if str(ee) not in str(e):
        continue
    break

assert 3 * e == 2 * (p-1) * (q-1) + 1
assert str(nn) in str(p * q)
assert str(ee) in str(e)
assert isPrime(p) and isPrime(q)
assert p.bit_length() == 512
assert q.bit_length() == 512
assert p != q
assert GCD(e, (p - 1) * (q - 1)) == 1 
assert 65537 < e < (p - 1) * (q - 1) - 65537

print(f'p = {p}')
print(f'q = {q}')
print(f'e = {e}')
# p = 8088430881271757130274784339253665338335626861355585318498924098872329526068810418778223672826275708502108494947472904429048917317830146855112324148596307
# q = 8000610987505880224296183684383189690409761101334714895423889508209590519034875705962809615495410114999121400419438307185857949951398310688366322313090379
# e = 43141592653589793238462643383279502884197169399375105820974944592307816406286012029957257665311892599272760841354029508833862170149297061469463995174000179889100502245620696926992798286112311731694241066719524989045789851259929870964395693863447149033024524160971530391030421457888460231006282766051743295779