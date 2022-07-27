from Crypto.Util.number import *
import random

data = open('stream_output.txt','r').read()
dataList = list(data)


N = len(data)
 
keyLen = N // 5 

a = data[N-8:]
key_bits = [0 for _ in range(keyLen)]

get_bits = [False for _ in range(keyLen)]
for i in range(0,N,8): ## all have to be printable
    key_bits[i % keyLen] = int(data[i])
    get_bits[i % keyLen] = True

def guess(idx, alphabet):
    global key_bits, get_bits
    base = ''
    for x in alphabet:
        base += "{:08b}".format(ord(x))
    for k in range(len(alphabet) * 8):
        tmp = int(data[idx + k]) ^ int(base[k])
        if get_bits[(idx + k) % keyLen] == True:
            assert key_bits[(idx + k) % keyLen] == tmp
        key_bits[(idx + k) % keyLen] = tmp
        get_bits[(idx + k) % keyLen] = True

idx = N - 8
guessKey = []
guess(N-1*8, '}')
guess(N-52*8, 'h')
guess(N-51*8, 'o')
guess(N-50*8, 'p')
guess(N-49*8, 'e')
guess(N-48*8, '{')

for i in range(52,0,-1):
    s = []
    for k in range(8):
        tmp = get_bits[(N-i*8 + k) % keyLen]
        s.append(tmp)

## my guess with eye
guess(2821 * 8, 'that his first son would be named Dudley. And I thought')

guess(5700 * 8, 'anything reasonable that he wanted, except, maybe, th')

guess(8575 * 8, ' up and wave a wand and magic would come out. The strang')

guess(11452 * 8, 'm the kitchen sink to stare at him, looking shocked')

guess(14331 * 8, 't."hope{that-was-very-rational-of-you_a')


##check how many alphabet is used
s = set()

plaintext_bits = []
st = False
store = ''
for i in range(len(data)):
    tmp = int(data[i]) ^ key_bits[i % keyLen]
    plaintext_bits.append(str(tmp))
    if (i % keyLen == idx % keyLen):
        st = True
        store =''
    
    if(st):
        store += str(tmp)
    if (i % keyLen == (idx + 7) % keyLen):
        st = False

plaintext = ''.join(plaintext_bits)
plain = long_to_bytes(int(plaintext,2))
print("==" * 4)
print("==" * 4)

s = set()

pr = ''
for i in range(0,N,8):
    check = True
    for k in range(8):
        if get_bits[(i +k) % keyLen] != True:
            check = False
    if check:
        idx = i // 8
        if(pr == ''):
            print(f'start : {idx}')
        pr += chr(plain[idx])
    else:
        if(pr != ''):
            print(f'end   : {idx}')
            print(f'"{pr}"')
            pr = ''
print(pr)