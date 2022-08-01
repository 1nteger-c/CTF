from Crypto.Util.number import inverse, long_to_bytes, isPrime
e = 65537
d = 195285722677343056731308789302965842898515630705905989253864700147610471486140197351850817673117692460241696816114531352324651403853171392804745693538688912545296861525940847905313261324431856121426611991563634798757309882637947424059539232910352573618475579466190912888605860293465441434324139634261315613929473
ct = 212118183964533878687650903337696329626088379125296944148034924018434446792800531043981892206180946802424273758169180391641372690881250694674772100520951338387690486150086059888545223362117314871848416041394861399201900469160864641377209190150270559789319354306267000948644929585048244599181272990506465820030285

# e * d = k * phi(n) + 1
kphin = e * d - 1

# e > k
## Round 1 : get phin
small_prime = [2, 3, 5, 7, 11, 13, 17][::-1]
phins = []
for k in range(1,e):
    if kphin % k != 0:
        continue
    phin = kphin // k
    flag = True
    check = False
    for i in range(len(small_prime)):
        if (flag and (phin % small_prime[i] == 0)):
            flag = False
        if ((not flag) and (phin % small_prime[i] != 0) ):
            check = True
            break
    if check:
        continue
    flag = True
    for i in range(len(small_prime)):
        tmp = small_prime[i] ** 2
        if (flag and (phin % tmp == 0)):
            flag = False
        if ((not flag) and (phin % tmp != 0) ):
            check = True
            break
    if check:
        continue
    for i in range(len(small_prime)):
        tmp = small_prime[i] ** 3
        if phin % tmp == 0:
            check = True
            break
    if check:
        continue
    phins.append(phin)
#print(phin)
#phin = 833231797337567181575506778941957841539063729789906303237664769112887205064268887620328583192911081430134120067558466226386762959265969633479467351396162451919343776941769879503288750483026728817053116542389709232171732928284059917356121270002980248517840758559619391795609522529482072609459709584022385507167700


## Round 2 : recover N
# I can factor phin using online calculator https://www.alpertron.com.ar/ECM.HTM
#2^2 × 3^2 × 5^2 × 7^2 × 11 × 10 357495 682248 249393 × 10 441209 995968 076929 × 10 476183 267045 952117 × 11 157595 634841 645959 × 11 865228 112172 030291 × 12 775011 866496 218557 × 13 403263 815706 423849 × 13 923226 921736 843531 × 14 497899 396819 662177 × 14 695627 525823 270231 × 15 789155 524315 171763 × 16 070004 423296 465647 × 16 303174 734043 925501 × 16 755840 154173 074063 × 17 757525 673663 327889 × 18 318015 934220 252801

p0 = 2 * 3 * 5 * 7 * 11
q0 = 2 * 3 * 5 * 7
primes = [10357495682248249393, 10441209995968076929, 10476183267045952117, 11157595634841645959, 11865228112172030291, 12775011866496218557, 13403263815706423849, 13923226921736843531, 14497899396819662177, 14695627525823270231, 15789155524315171763, 16070004423296465647, 16303174734043925501, 16755840154173074063, 17757525673663327889, 18318015934220252801]
assert len(primes) == 16

from itertools import combinations
from math import prod
for l in list(combinations(primes, 8)):
    p = prod(l) * p0 + 1
    q = (phin // (p-1)) + 1
    if (q-1) % q0 != 0:
        continue
    if isPrime(p) != True:
        continue
    if isPrime(q) != True:
        continue
    N = p * q
    m  = pow(ct, d, N)
    try:
        if long_to_bytes(m).decode().isprintable():
            print(long_to_bytes(m))
    except:
        pass

#flag : uiuctf{bru4e_f0rc3_1s_FUn_fuN_Fun_f0r_The_whOLe_F4miLY!}