from dataclasses import replace


f = open('output.txt')
ciphertext = f.read()[:-1]

replacement = dict()

characters = [' ', '"', ',', '.', 'A', 'B', 'E', 'I', 'M', 'O', 'S', 'T', 'V', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', '{', '}']

shuffled = [' ', '"', ',', '.', 'A', 'B', 'E', 'I', 'M', 'O', 'S', 'T', 'V', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', '{', '}']

def make(a,b):
    global replacement, shuffled
    for i in range(len(b)):
        replacement[a[i]] = b[i]
        shuffled.remove(b[i])


## just guess
make('hwfyAu', 'hope{}')
make('_"M}g', 'sagm ')
make('VdkBSlsq.', 'vdt.nucir')
make('Tijo,','_lbAx')
make('rtaEc ',',yBkfw')
make('xvpnbO{m','IMOE"VTS')
unknown = []
idx = 0
for i in range(len(characters)):
    if characters[i] in replacement.keys():
        continue
    replacement[characters[i]] = shuffled[idx]
    unknown.append(characters[i])
    idx += 1


plaintext = ''.join(replacement.get(c, c) for c in ciphertext)
with open('flag.txt','w') as f:
    f.write(plaintext)


print(unknown)
print(shuffled)
find = 'j'
for x in replacement.keys():
    if replacement[x] == find:
        print('got : ',x)