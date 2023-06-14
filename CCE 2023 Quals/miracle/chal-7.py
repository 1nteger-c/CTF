import os 
import random as rand
from Crypto.Util.number import GCD, isPrime 

print("Send Parameters!")
p = int(input())
q = int(input())
e = int(input())
n = p * q 

def validate(p, q, e, n):
    assert isPrime(p) and isPrime(q)
    assert p.bit_length() == 512
    assert q.bit_length() == 512
    assert p != q
    assert GCD(e, (p - 1) * (q - 1)) == 1 
    assert 65537 < e < (p - 1) * (q - 1) - 65537
    assert "3141592653589793238462643383279502884197169399375105820974944592307816406286" in str(e) # first digits of pi - nothing up my sleeve!
    assert "2718281828459045235360287471352662497757247093699959574966967627724076630353" in str(n) # first digits of E - nothing up my sleeve!

print("Validation!")
validate(p, q, e, n)

def inc_state(state):
    next_z = pow(state, e, n)
    next_out = next_z % (1 << 896)
    next_state = next_z >> 896 
    return next_out, next_state

state = rand.randint(1, n >> 896)
next_out, state = inc_state(state)

print("First Outputs")
print(next_out)

next_out, state = inc_state(state)

claimed_next_out = int(input())
claimed_state = int(input())

if claimed_next_out == next_out and claimed_state == state:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "flag.txt")) as f:
        FLAG = f.read().strip()
    print(FLAG)