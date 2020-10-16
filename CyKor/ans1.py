import base64
from math import gcd
from Crypto.Util.number import inverse
def affine(cipher,key1,key2):
    plain = ''
    
    for i in range(len(cipher)):
        tmp = cipher[i]
        if(tmp.isupper()):
            tmp = ord(tmp) - ord('A')
            tmp = (tmp-key2) * inverse(key1,26) 
            tmp = tmp % 26 + ord('A')
            plain += chr(tmp)
        elif(tmp.islower()):
            tmp = ord(tmp) - ord('a')
            tmp = (tmp-key2) * inverse(key1,26)
            tmp = tmp % 26 + ord('a')
            plain += chr(tmp)
        else:
            plain += tmp
    print (plain , key1 , key2)
    
with open('crypto_easy.txt','r') as f:
    cipher = f.read()

cipher = base64.b64decode(cipher).decode()

cip = cipher[6:-1]
for i in range(26):
    for j in range(26):
        if(gcd(i,26) == 1):
            affine(cip,i,j)