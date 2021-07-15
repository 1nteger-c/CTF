import random

def untemper(inp):
    # start to recover random
    y = inp

    #y ^= (y >> 18)
    tmp0 = (y >> 14) << 14 
    tmp1 = y >> 18
    y = tmp0 | ((y ^ tmp1) & ( (1 << 14) - 1))

    #y ^= (y << 15) & 0xefc60000
    tmp0 = y & ((1 << 17)-1)
    tmp1 = tmp0 << 15
    y = y ^ (tmp1 & 0xefc60000)

    #y ^= (y << 7) & 0x9d2c5680

    tmp0 = y & ((1 << 7) - 1) 
    tmp2 = tmp0
    for i in range(1,5):
        tmp1 = (tmp2 << 7) & 0x9d2c5680
        tmp2= (y ^ tmp1) & (((1 << 7)-1) << (7 * i))
        tmp0 += tmp2
    y = tmp0
    #y ^= (y >> 11)
    tmp0 = (y >> 21) << 21 
    tmp2 = tmp0
    tmp1 = tmp2 >> 11
    tmp2 = (tmp1 ^ y) & (((1 << 11)-1)<<10)
    tmp0 += tmp2
    tmp1 = tmp2 >> 11
    tmp2 = (tmp1 ^ y) & ((1 <<10)-1)
    tmp0 += tmp2
    y = tmp0

    a = y ^ (y >> 11)
    a ^= (a << 7) & 0x9d2c5680
    a ^= (a << 15) & 0xefc60000
    a ^= (a >> 18)

    return y
state = random.getstate()

rands = [0 for i in range(1000)]
for i in range(len(rands)):
    rands[i] = random.getrandbits(32)  # make random

recovered_state = (3, tuple([ untemper(v) for v in rands[:624] ] + [0]), None)
random.setstate(recovered_state)

for i in range(1000):  ## check !
    t = random.getrandbits(32)
    assert t == rands[i]
