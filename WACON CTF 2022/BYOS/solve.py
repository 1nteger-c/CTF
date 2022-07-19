import random
from pwn import *
from itertools import product
BLOCK_SIZE = 24
SBOX_SIZE = 12

s = set(i for i in range(12))
def find_seed():
    seed = 0
    while(1):
        random.seed(seed)
        perm = list(range(BLOCK_SIZE))
        random.shuffle(perm)
        if(set(perm[:12]) == s):
            print(f'[*] special seed : {seed}')
            return seed
        seed += 1

def addkey(block, key):
    return block ^ key

def substitution(block):
    s = SBOX[block]
    return s

def permutation(perm, block):
    bits = bin(block)[2:].zfill(SBOX_SIZE)
    bits = ''.join(bits[perm[i]] for i in range(SBOX_SIZE))
    return int(bits, 2)

def solve(data, perm_DB, perm_DB_inv, SBOX, SBOX_inv):
    keys = []
    for key1, key3 in product(range(1 << SBOX_SIZE), repeat = 2):
        key2 = set()
        for (pt, ct) in data:
            block1 = addkey(pt, key1)
            block1 = SBOX[block1]
            block1 = perm_DB[block1]

            block2 = addkey(ct, key3)
            block2 = perm_DB_inv[block2]
            block2 = SBOX_inv[block2]
            key2.add(block1 ^ block2)
        if len(key2) == 1:
            keys = [key1, key2.pop(), key3]
            return keys



# seed = find_seed() # 499140
seed = 499140
random.seed(seed)

perm = list(range(BLOCK_SIZE))
random.shuffle(perm)

perm1 = perm[ : SBOX_SIZE]
perm2 = [perm[i] - SBOX_SIZE for i in range(SBOX_SIZE, SBOX_SIZE * 2)]


SBOX = list(range(1 << SBOX_SIZE))
random.shuffle(SBOX)

SBOX_inv = [SBOX.index(i) for i in range(1 << SBOX_SIZE)]

##perm DB
perm1_DB = [permutation(perm1, i) for i in range(1 << SBOX_SIZE)]
perm2_DB = [permutation(perm2, i) for i in range(1 << SBOX_SIZE)]
perm1_DB_inv = [perm1_DB.index(i) for i in range(1 << SBOX_SIZE)]
perm2_DB_inv = [perm2_DB.index(i) for i in range(1 << SBOX_SIZE)]



r = process(['python3','prob.py'])

r.recvuntil(b'> ')

r.sendline(str(seed).encode())

data1 = []
data2 = []
for i in range(10):
    r.recvuntil(b'> ')
    plain = (i << SBOX_SIZE) | i
    r.sendline(str(plain).encode())
    cipher = int(r.recvline()[:-1].decode())
    c1 = cipher >> SBOX_SIZE
    c2 = cipher % (1 << SBOX_SIZE)
    data1.append([i, c1])
    data2.append([i, c2])

## solve
k1 = solve(data1, perm1_DB, perm1_DB_inv, SBOX, SBOX_inv)
print(k1)
k2 = solve(data2, perm2_DB, perm2_DB_inv, SBOX, SBOX_inv)
print(k2)

keys = []
for i in range(3):
    key = (k1[i] << SBOX_SIZE) + k2[i]
    r.recvuntil(b'> ')
    r.sendline(str(key).encode())

r.interactive()