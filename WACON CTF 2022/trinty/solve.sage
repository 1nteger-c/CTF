"""
This code finds unknown MSBs of dp, dq 
when LSBs of dp & dq are known using our idea. It will reproduce Table 2 and Table 3 of our paper.
"""

m_1 = 5 #Parameter for 1st Lattice
m_2 = 14 #Parameter for 2nd Lattice
t_2 = 7 #Parameter for 2nd Lattice

# n is the size of primes, alpha is the size of e. dSize is bit size of dp & dq. Number of unknown bits of dp & dq is Unknown_MSB.

n = 512 
dSize = 512
alpha = 85
Unknown_MSB = 312

#TWO_POWER is the left shift of 2. This value corresponds  to the knowledge of LSBs
TWO_POWER = 2^(dSize - Unknown_MSB)

#keyGen function generates CRT-RSA parameters. 

"""
N,e,LSB_dp, LSB_dq are known to the attacker. 
p,q,dp,dq,MSB_dp,MSB_dq,k,l are unknown. Attacker first tries to 
find k and l using lattice reduction. Then uses the knowledge of k to find MSB_dp 
""" 

N = 150521291786162634207005525778169708708522720074345927077420731185600563387046639806238339255757863868699490815776623273376348175253988894743885370764780600900302789673531599439459445183505805277387459741112034759427671859796591301689098407566045632882616152019038756129184959273344103972335895300046311701809
e = 30510532618964464063517147
LSB_dp = 1277251830107045061098265337744483546719636547425635587593463
LSB_dq = 230441702892751221228737480414520264502429400074470159039659


A = -e^2* LSB_dp* LSB_dq+e* LSB_dp+e* LSB_dq-1

B = gcd(N-1,e*TWO_POWER)

C = (N-1)/B
C = ZZ(C)

C_IN = C.inverse_mod(e*TWO_POWER)

C_IN = ZZ(C_IN)
R.<x,y>=QQ[]

f = B*x*y-C_IN*(e*LSB_dq-1)*x-C_IN*(e*LSB_dp-1)*y+A*C_IN  #(k,l) is a root of f modulo e*TWO_POWER

# X and Y are upper bounds of  k and l respectively 
X = 2^alpha
Y = 2^alpha

"""
We store shift polynomials in set G and all monomials of shift polynomials in MON
"""
G = []
MON = []
for a in range(m_1+1):
   for b in range(m_1+1):
     MON.append(x^a*y^b)
     if(a>=b):
        g = x^(a-b)*f^b*(e*TWO_POWER)^(m_1-b)
     else:
        g = y^(b-a)*f^a*(e*TWO_POWER)^(m_1-a)

     g = g(x*X,y*Y)
     G.append(g)
  
"""
Form a matrix B_LSB. Entries of B_LSB are coming from the coefficient 
vector from  shift polynomials
""" 

B_LSB = zero_matrix(ZZ,(m_1+1)^2) 
print('1st lattice dimension', (m_1+1)^2)
for j in range(len(G)):
    for i in range(len(MON)):
        cij = (G[j]).coefficient(MON[i])
        cij = cij(0,0)
        B_LSB[j,i] = cij

#Apply LLL algorithm over the matrix B_LSB
B_LSB = B_LSB.LLL()
"""
After reduction, now we are reconstructing the 
polynomials from the matrix and these polynomials have common root (k,l) over integer. 
These polynomials correspond to shorter vectors in the lattice. We store these polynomials in a set POLY
"""
POLY = []
val = (m_1+1)^2

M = Matrix(val-1)
ans = Matrix(val-1,1)
POLY = []

for j in range(val-1):
    f = 0
    for i in range(val):
        cij = B_LSB[j,i]
        cij = cij/MON[i](X,Y)
        cj = ZZ(cij)
        f = f + cj*MON[i]
    coeff = f.coefficients()
    M[j] = coeff[:-1]
    ans[j,0] = coeff[-1] * -1
    assert len(coeff) == 36

set_verbose(-1)

res = M.inverse() * ans
k = res[-2][0]
l = res[-1][0]

k = Integer(int(k))
l = Integer(int(l))
# print(k,l)

"""
We compute  Grobner basis over prime field Z instead of over integers for efficiency. Since k, l are less
than e, we take Z as the next prime of e
We consider the polynomials of POLY as modular polynomials over GF(Z). Then 
try to find the root using Groebner basis.
""" 
Z = next_prime(e)
MOD = PolynomialRing(GF(Z), 2, 'X')
POLY_NEW = []
for i in range(len(POLY)):
      POLY_NEW.append(MOD(POLY[i]))

R.<x>=QQ[]
f = (e*(TWO_POWER*x+LSB_dp)-1+k)
IN_k = (e*TWO_POWER).inverse_mod(k*N)

f = x+IN_k*(e*LSB_dp-1+k) # Make f monic by inverting the coefficient of x
X = 2^Unknown_MSB


#Generate shift polynomials and store these polynomials in F. Store monomials of shift polynomials in S 
F = []
S = []
for i in range(m_2+1):
    h = f^i*k^(m_2-i)*N^(max(0,t_2-i))
    F.append(h)
    S.append(x^i)

"""
Form a matrix MAT. Entries of MAT are coming from the coefficient 
vector from shift polynomials which are stored in F
""" 

MAT = Matrix(ZZ, len(F))

for i in range(len(F)):
   f = F[i]
   f = f(x*X)

   coeffs = (f.coefficients(sparse=False))
   for j in range(len(coeffs), len(F)):
       coeffs.append(0)
   coeffs = vector(coeffs)
   MAT[i] = coeffs


MAT = MAT.LLL()

#After reduction identify polynomials which have root MSB_dp over integer and store them in a set A. 

A = []

for j in range(len(F)-1):
    f = 0
    for i in range(len(S)):
        cij = MAT[j,i]
        cij = cij/S[i](X)
        cj = ZZ(cij)
        f = f + cj*S[i]
    A.append(f)    
#Find the root MSB_dp using Groebner basis techenique over integer 
# print(A)
I = ideal(A)
B = I.groebner_basis()

MSB_dp = B[0].roots()[0][0]

dp = (MSB_dp << 200) + LSB_dp

#k = (e*dp-1)/(p-1)
p = ((e * dp - 1) / k) + 1
assert N % p == 0

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
q = N // p
p = int(p)
q = int(q)
e = int(e)
d = inverse(e,(p-1) * (q-1))
key = RSA.construct((int(N),int(e),int(d)))

c = 0x9118ecc4581f2f200a07a34f64ec91caca2a2adbead4509311af96e76ccecbd042ea284c382b2caf40528c3c86d98f6e9c62c5f72d6e12a8a932f26ac2e32ab86ab85c64919c86a8c2632f5a625d6292947b5f59fb443f672a4e9047e2cb9e6d90e0fd81ac016ea03ed79269b8fbe9c442bd7d77e9278b15dde31f2adc920bd1
c = long_to_bytes(c)
cipher = PKCS1_OAEP.new(key)
print(cipher.decrypt(c))