from output import *
from Crypto.Util.number import *
from pwn import *
class LCG:
    def __init__(self, a, x, b, q):
        self.a = a
        self.x = x 
        self.b = b 
        self.q = q
    def fetch(self):
        ret = self.x
        self.x = (self.a * self.x + self.b) % self.q 
        return ret 

r = process(['python3','chal.py'])

def sl(x):
    r.sendline(str(x).encode())
    sleep(0.5)

q = int(r.recvline()[4:])
log.info(f'q : {q}')
r.recvline()
a = random.randint(1, q-1)
sl(a)
x = random.randint(1, q-1)
sl(x)
b = random.randint(1, q-1)
sl(b)
ns = []
for i in range(4):
    ns.append(int(r.recvline()))
log.info('start')

LCG1 = LCG(a, x, b, q)
# LCG1_u1 / LCG1_v1
# LCG1_u2 / LCG1_v2

us, vs = [], []
outs = [LCG1.fetch() for _ in range(30000)]
i = 0
while(len(us) < 4):
    t = (ns[len(us)] % q) * inverse(outs[i], q) % q
    if t in outs:
        j = outs.index(t)
        us.append(i)
        vs.append(j)
        i = j
    i += 1
log.info(f'us : {us}')
log.info(f'vs : {vs}')
# memo for solve
'''
LCGi_j (i : 1, 2, 3)
LCGi_0 = xi
LCGi_1 = ai * xi + bi
LCGi_2 = ai^2 * xi + bi(ai + 1)
LCGi_j = ai^j * xi + bi(ai^j - 1) / (ai - 1)
       = ai^j ( xi + bi / (ai - 1)) - bi / (ai - 1)
       = ai^j * C + D   mod q !!
'''
# n1 (mod q^2)  = (LCG2_u0 * q + LCG1_u0) * (LCG2_v0 * q + LCG1_v0)
#               = (LCG1_v0 * LCG2_u0 + LCG1_u0 * LCG2_v0) * q + LCG1_u0 * LCG1_v0

# (n1 - (LCG1_u0 * LCG1_v0)) / q = LCG1_v0 * LCG2_u0 + LCG1_u0 * LCG2_v0    (mod q)
# (LCG1_v0 * a2^u0 + LCG1_u0 * a2^v0) * C + (LCG1_v0 + LCG1_u0) * D - (n1 - (LCG1_u0 * LCG1_v0)) / q
Fp = PolynomialRing(Zmod(q), 'a2')
a2 = Fp.gen()

M1 = Matrix(Fp, 3)
for i in range(3):
    M1[i, 0] = outs[vs[i]] * a2^us[i] + outs[us[i]] * a2 ^ vs[i]
    M1[i, 1] = outs[us[i]] + outs[vs[i]]
    M1[i, 2] = (ns[i] - (outs[us[i]] * outs[vs[i]])) //  q

M2 = Matrix(Fp, 3)
for i in range(1, 4):
    M2[i - 1, 0] = outs[vs[i]] * a2^us[i] + outs[us[i]] * a2 ^ vs[i]
    M2[i - 1, 1] = outs[us[i]] + outs[vs[i]]
    M2[i - 1, 2] = (ns[i] - (outs[us[i]] * outs[vs[i]])) //  q

d1 = M1.det()
d2 = M2.det()

while(d2 != Fp(0)):
    d1, d2 = d2, d1 % d2
# x2 = C + D
# b2 = -1 * (a2 - 1) * D

a2_cand = d1.roots()[0][0]
Fp2.<C,D> = PolynomialRing(Zmod(q))
f1 = Fp2(M1[0,0](a2_cand)) * C + Fp2(M1[0,1]) * D - Fp2(M1[0,2])
f2 = Fp2(M1[1,0](a2_cand)) * C + Fp2(M1[1,1]) * D - Fp2(M1[1,2])
g1 = f1 * f2.coefficients()[0] - f2 * f1.coefficients()[0]
D = (g1.coefficients()[1] * -1) / g1.coefficients()[0]
g2 = f1(D=D)
C = (g2.coefficients()[1] * -1) / g2.coefficients()[0]

a2 = a2_cand
x2 = C + D
b2 = -1 * (a2 - 1) * D
# ## recover a2, x2, b2
LCG2 = LCG(Integer(a2), Integer(x2), Integer(b2), q)

# ### Start => Coppersmith Attack
LCG1s, LCG2s = [], []
outs2 = [LCG2.fetch() for _ in range(vs[-1] + 1)]
for i in range(len(us)):
    LCG1s.append(outs[us[i]])
    LCG2s.append(outs2[us[i]])

partialPrimes = [LCG1s[i] + LCG2s[i] * q for i in range(len(LCG1s))]

factor = []
for i in range(4):
    Pr.<x> = PolynomialRing(Zmod(ns[i]))
    f = x * q * q + partialPrimes[i]
    f = f.monic()
    res = f.small_roots(X=q, beta=0.4)
    if len(res) != 0:
        x = int(res[0])
        p = x * q^2 + partialPrimes[i]
        assert ns[i] % p == 0
        factor.append(p)
        factor.append(ns[i] // p)

log.info('[+] factor Done')
for i in range(4):
    sl(factor[2 * i])
    sl(factor[2 * i + 1])

r.interactive()