from hashlib import sha256
from Crypto.Util.number import inverse,GCD

ha = lambda x: x if isinstance(x, int) or isinstance(x, Integer) else product(x.xy())
hashs = lambda *x: int.from_bytes(sha256(b'.'.join([b'%X' % ha(x) for x in x])).digest(), 'little') % p



ec = EllipticCurve(GF(2**255-19), [0, 486662, 0, 1, 0])
# y^2 = x^3 + 486662*x^2 + x
p = ec.order()
ZmodP = Zmod(p)
G = ec.lift_x(9)
Gx = 9
Gy =43114425171068552920764898935933967039370386198203806730763910166200978582548

def hashp(x):
    x = hashs((x))
    while True:
        try:
            return ec.lift_x(x)
        except:
            x = hashs((x))

def verify(signature, P, m):
    I, e, s = signature
    return e == hashs(m, s*G + e*P, s*hashp(P) + e*I)


I = ec.lift_x(1)

n =ec.order()


P = ec(33248629177511128698718614525296568668566983572474077066896686389501073172020,53920302129363286902767591465643933467289570525885710658900051857303537860120)
m = 22934736172478986380900580990804025962897141062815346200065868089362579013556
x = 12267717851567050600497355603269368910251453540292888097922387111714860194190
#k = (s+ex )*G
a = 2
i_list = []
s_list = []
e_list = []
A = hashp(P)
for a in range(100):
    e = 20432330436901099429713209161828846337430074069792130639558483985289039922356
    s = (n +1- e * x)
    
    I = (x + inverse(e,n) * a)*A
    k = hashs(m,G,A*(2*a+1))
    
    e = k
    s = (n +1- e * x)
    I = (x + inverse(e,n) * a)*A
    if (verify((I, e, s), P, m)) and I not in i_list:
        i_list.append(I)
        s_list.append(s)
        e_list.append(e)
        if(len(i_list) == 8):
            break

print(len(i_list))
for i in range(8):
    print(i_list[i],s_list[i],e_list[i])
