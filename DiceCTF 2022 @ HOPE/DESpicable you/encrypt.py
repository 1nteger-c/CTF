from os import urandom

def encipher(a,b):
    c = ''
    print(a)
    print(b)
    for i, j in zip(a,b):
        c+=chr(ord(i) ^ j)
    return c

def rekey(key):
    k = b""
    for i,c in enumerate(key):
        # print(c)
        if i == len(key)-1:
            k += chr(c).encode()
            k += chr(c^key[0]).encode()
        else:
            k += chr(c).encode()
            k += chr(c^key[i+1]).encode()
    key = k

def main():
    key = urandom(8)


    plaintext = 'hope{asdasdasaa}'
    i = 0
    ct = ''
    while i < len(plaintext):
        ct += encipher(plaintext[i:i+len(key)],key)
        i += len(key)
        rekey(key)
        print('key :',key)
    print(ct)

main()

