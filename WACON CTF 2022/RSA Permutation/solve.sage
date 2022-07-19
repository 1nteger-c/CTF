from itertools import product
from pwn import *
import hashlib
def mapped(s, perm):
    ret = ""
    for x in s:
        ret += hex(perm[int(x, 16)])[2:]
    return ret


# check using bits
# condition :
# N = p * q
# e * dp = kp * (p-1) + 1
# e * dq = kq * (q-1) + 1
# mod 2^x
def check(N, _p, _q, _dp, _dq, e, kp, kq, bits):
    p = int(''.join(_p[:bits])[::-1],2)
    q = int(''.join(_q[:bits])[::-1],2)
    dp = int(''.join(_dp[:bits])[::-1],2)
    dq = int(''.join(_dq[:bits])[::-1],2)
    mod = pow(2,bits)
    if((p * q) % mod != N % mod):
        return False
    if((e * dp) % mod != (kp * (p-1) + 1) % mod):
        return False
    if((e * dq) % mod != (kq * (q-1) + 1) % mod):
        return False
    return True


def check2(dp, p_dp, permutation, bits):
    check_bit = ((bits -1) % 4) + 1
    permutated_dp = int(p_dp[(bits - 1) // 4],16)
    if(permutation[permutated_dp] != -1):
        current_val = int(''.join(dp[bits - check_bit : bits][::-1]),2)
        if (current_val != (permutation[permutated_dp] % (1 << check_bit))):
            return False
    return True

def rollback_data(p, q, dp, dq, permutation, bits, setting):
    p[bits] = None
    q[bits] = None
    dp[bits] = None
    dq[bits] = None
    for x in setting:
        permutation[x] = -1

def recover(p, q, dp, dq, e, bits, kp, kq, p_dp, p_dq, N, permutation):
    global answer_perm
    if(bits == 500):
        print("[*] recovered permutation array")
        return permutation
    # same as permutation table?
    if(not check2(dp, p_dp, permutation, bits)):
        return False
    if(not check2(dq, p_dq, permutation, bits)):
        return False
    valid_dp = ['0','1']
    valid_dq = ['0','1']
    ## set data
    permutated_dp = int(p_dp[(bits) // 4],16)
    if(permutation[permutated_dp] != -1):
        valid_dp = [str((permutation[permutated_dp] >> ((bits) % 4)) & 1)]
        
    permutated_dq = int(p_dq[(bits ) // 4],16)
    if(permutation[permutated_dq] != -1):
        valid_dq = [str((permutation[permutated_dq] >> ((bits) % 4)) & 1)]


    setting = []
    ## set permutation
    if bits % 4 == 0:
        permutated_dp = int(p_dp[(bits - 1) // 4],16)
        if(permutation[permutated_dp] == -1):
            val = int(''.join(dp[bits-4:bits][::-1]),2)
            if val in permutation:
                rollback_data(p, q, dp, dq, permutation, bits, setting)
                return False
            permutation[permutated_dp] = val
            setting.append(permutated_dp)
        permutated_dq = int(p_dq[(bits - 1) // 4],16)
        if(permutation[permutated_dq] == -1):
            val = int(''.join(dq[bits-4:bits][::-1]),2)
            if val in permutation:
                rollback_data(p, q, dp, dq, permutation, bits, setting)
                return False
            permutation[permutated_dq] = val
            setting.append(permutated_dq)

    #add
    valid_p = ['0','1']
    valid_q = ['0','1']
    for pbit, qbit, dpbit, dqbit in product(valid_p, valid_q, valid_dp, valid_dq):
        p[bits] = pbit
        q[bits] = qbit
        dp[bits] = dpbit
        dq[bits] = dqbit
        if(check(N, p, q, dp, dq, e, kp, kq, bits + 1)): #check 1
            if(recover(p, q, dp, dq, e, bits+1, kp ,kq, p_dp, p_dq, N, permutation)):
                return permutation

    rollback_data(p, q, dp, dq, permutation, bits, setting)
    return False

r = process(['python3','chal.py'])
r.recvline()
s = r.recvline()[:-1].decode()

for i in range(1 << 28):
    t = str(i)
    hash = hashlib.sha256((s + t).encode()).hexdigest()
    if hash[:6] == "000000": 
        r.sendline(t.encode())
        break
    
N = eval(r.recvline())
recv_p_dp = r.recvline()[:-1].decode()
recv_p_dq = r.recvline()[:-1].decode()

p_dp = list(recv_p_dp)[::-1]
p_dq = list(recv_p_dq)[::-1]

e = 293
for k in range(e,0,-1):
    print(f'checking for k : {k}')
    x = Zmod(e)["x"].gen()
    f = x ** 2 - x * (k * (N - 1) + 1) - k
    try:
        kp, kq = f.roots(multiplicities=False)
    except:
        continue
    kp = int(kp)
    kq = int(kq)
    p = [None for _ in range(1024)]
    q = [None for _ in range(1024)]
    dp = [None for _ in range(1024)]
    dq = [None for _ in range(1024)]
    p[0] = '1'
    q[0] = '1'
    dp[0] = '1'
    dq[0] = '1'
    bits = 1
    permutation = [-1 for _ in range(16)] 
    perm = recover(p, q, dp, dq, e, bits, kp, kq, p_dp, p_dq, N, permutation)
    if(perm == False):
        continue
    dp = int(mapped(recv_p_dp, perm),16)
    dq = int(mapped(recv_p_dq, perm),16)

    # e * dp = kp * (p-1) + 1
    # e * dq = kq * (q-1) + 1
    p = (e * dp - 1) // kp + 1
    q = (e * dq - 1) // kq + 1
    if p * q == N:
        print("[*] FIND ANSWER")
        r.sendline(str(p).encode())
        sleep(0.01)
        r.sendline(str(q).encode())
        r.interactive()

