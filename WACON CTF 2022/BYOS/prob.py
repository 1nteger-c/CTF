#!/usr/bin/python3
import random
import os
# import signal

# signal.alarm(600)

BLOCK_SIZE = 24
SBOX_SIZE = 12
FLAG = open("flag.txt").read()

seed = int(input('BYOS(Bring Your Own Seed) > '))
random.seed(seed)

perm = list(range(BLOCK_SIZE))
random.shuffle(perm)

SBOX = list(range(1 << SBOX_SIZE))
random.shuffle(SBOX)

print("partial SBOX & permutation(Do not doubt server :p)")
print("partial SBOX", SBOX[:24])
print("permutation", perm)

def addkey(block, key):
    return block ^ key

def substitution(block):
    s1 = SBOX[block >> SBOX_SIZE]
    s2 = SBOX[block & ((1 << SBOX_SIZE) - 1)]
    return (s1 << SBOX_SIZE) | s2

def permutation(block):
    bits = bin(block)[2:].zfill(BLOCK_SIZE)
    bits = ''.join(bits[perm[i]] for i in range(BLOCK_SIZE))
    return int(bits, 2)

def enc(plaintext, key1, key2, key3):
    block = addkey(plaintext, key1)
    block = substitution(block)
    block = permutation(block)

    block = addkey(block, key2)
    block = substitution(block)
    block = permutation(block)

    block = addkey(block, key3)
    return block

key1 = int.from_bytes(os.urandom(3), 'big')
key2 = int.from_bytes(os.urandom(3), 'big')
key3 = int.from_bytes(os.urandom(3), 'big')

for _ in range(10):
    plaintext = int(input("plaintext > "))
    assert(0 <= plaintext < (1 << BLOCK_SIZE))
    print(enc(plaintext,key1,key2,key3))

assert(key1 == int(input("key1? > ")))
assert(key2 == int(input("key2? > ")))
assert(key3 == int(input("key3? > ")))

print("Good job!, flag is", FLAG)