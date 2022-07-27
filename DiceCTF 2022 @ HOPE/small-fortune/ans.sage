from Crypto.Util.number import *

f = open('output.txt','r')
n = eval(f.readline().split('=')[1])
x = eval(f.readline().split('=')[1])
enc = eval(f.readline().split('=')[1])

R = Zmod(n)
P.<delta> = PolynomialRing(R)


y2 = (inverse(x,n) * enc[0]) % n
flag = '1'
for c in enc[1:]:
    print(f"Recovering ... {len(flag)}")
    get = False
    for b in [0,1]:
        a = (c * inverse(x^b,n) - y2) % n
        f = (a - delta^2)^2 - 4 * y2 * delta^2
        f = f.monic()
        r = f.small_roots()
        if(len(r) == 0):
            pass
        else:
            if get == True:
                print("Something Wrong")
            flag = str(b) + flag
            get = True
    if(get == False):
        print("Something Wrong")
    if len(flag) % 8 == 0:
        print(long_to_bytes(int(flag,2)))
print(b'flag : ',long_to_bytes(int(flag,2)))
#hope{r4nd0m_sh0uld_b3_truly_r4nd0m_3v3ry_t1m3_sh0uld_1t_n0t?}