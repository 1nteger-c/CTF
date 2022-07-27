from Crypto.Util.strxor import strxor

f = open('output.txt','rb')
ciphertext = f.read()[:-1]

flag = b'hope{'



key5 = strxor(ciphertext[:5],flag)
plain = b''
i = 0 
key = key5 + b'\x6e' + b'\xc1' + b'\x61'

while(i < len(ciphertext)):
    plain += strxor(ciphertext[i:i+len(key)],key)
    i += 8

print(plain)