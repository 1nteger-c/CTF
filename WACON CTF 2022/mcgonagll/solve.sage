from pwn import *
import random

from fpylll import LLL, BKZ, IntegerMatrix
import ecdsa_lib


def reduce_lattice(lattice, block_size=None):
    if block_size is None:
        print("LLL reduction")
        return LLL.reduction(lattice)
    print(f"BKZ reduction : block size = {block_size}")
    return BKZ.reduction(
        lattice,
        BKZ.Param(
            block_size=block_size,
            strategies=BKZ.DEFAULT_STRATEGY,
            auto_abort=True,
        ),
    )


def test_result(mat, target_pubkey, curve):
    mod_n = ecdsa_lib.curve_n(curve)
    for row in mat:
        candidate = row[-2] % mod_n
        if candidate > 0:
            cand1 = int(candidate)
            cand2 = int(mod_n - candidate)

            if target_pubkey == ecdsa_lib.privkey_to_pubkey(cand1, curve):
                return cand1
            if target_pubkey == ecdsa_lib.privkey_to_pubkey(cand2, curve):
                return cand2
    return 0

def build_matrix(sigs, curve, num_bits, bits_type):
    num_sigs = len(sigs)
    n_order = ecdsa_lib.curve_n(curve)
    curve_card = 2 ** ecdsa_lib.curve_size(curve)
    lattice = IntegerMatrix(num_sigs + 2, num_sigs + 2)
    kbi = 2 ** num_bits
    inv = ecdsa_lib.inverse_mod
    if bits_type == "LSB":
        pass
    else:
        # MSB
        for i in range(num_sigs):
            lattice[i, i] = 2 * kbi * n_order
            hash_i = sigs[i]["hash"]
            lattice[num_sigs, i] = (
                2 * kbi * ((sigs[i]["r"] * inv(sigs[i]["s"], n_order)) % n_order)
            )
            lattice[num_sigs + 1, i] = (
                2
                * kbi
                * (
                    sigs[i]["kp"] * (curve_card // kbi)
                    - hash_i * inv(sigs[i]["s"], n_order)
                )
                + n_order
            )
    lattice[num_sigs, num_sigs] = 1
    lattice[num_sigs + 1, num_sigs + 1] = n_order
    return lattice


MINIMUM_BITS = 4
RECOVERY_SEQUENCE = [None, 15, 25, 40, 50, 60]
SIGNATURES_NUMBER_MARGIN = 1.03


def minimum_sigs_required(num_bits, curve_name):
    curve_size = ecdsa_lib.curve_size(curve_name)
    return int(SIGNATURES_NUMBER_MARGIN * 4 / 3 * curve_size / num_bits)


def recover_private_key(
    signatures_data, pub_key, curve, bits_type, num_bits
):

    # Is known bits > 4 ?
    # Change to 5 for 384 and 8 for 521 ?
    if num_bits < MINIMUM_BITS:
        return False

    # Is there enough signatures ?
    n_sigs = minimum_sigs_required(num_bits, curve)
    if n_sigs > len(signatures_data):
        return False


    sigs_data = random.sample(signatures_data, n_sigs)

    print("Constructing matrix")
    lattice = build_matrix(sigs_data, curve, num_bits, bits_type)

    print("Solving matrix ...")
    for effort in RECOVERY_SEQUENCE:
        lattice = reduce_lattice(lattice, effort)
        res = test_result(lattice, pub_key, curve)
        if res:
            return res
    return 0


from pwn import *
from Crypto.Util.number import *
from hashlib import sha1

#r = remote('175.123.252.186', 13337)
r = process(['python3','chall.py'])
s = r.recvline()[:-1].decode()

print(s)
for i in range(1 << 28):
    t = str(i)
    hash = hashlib.sha256((s + t).encode()).hexdigest()
    if hash[:6] == "000000": 
        r.sendline(t.encode())
        break
print("START")
suc = 0
for times in range(30):
    print("START : ",times + 1)
    sk_x = int(r.recvline())
    sk_y = int(r.recvline())

    sig_data = []
    for i in range(256): 
        msg, sig, klen = r.recvline()[:-1].decode().split(' ')
        # print(msg)
        klen = int(klen)
        msg = bytes.fromhex(msg)
        h = sha1(msg).digest()
        # print(h)
        h = bytes_to_long(h)
        _r = int(sig[:64],16)
        _s = int(sig[64:],16)
        sig = int(sig ,16)
        js = {}
        if(klen <= 252):
            js["hash"] = h
            js["r"] = _r
            js["s"] = _s
            js["kp"] = 0
            sig_data.append(js)
    res = recover_private_key(sig_data,[sk_x,sk_y], "SECP256K1", "MSB", 4)
    if res != 0:
        suc += 1
        print("TIMES : ",suc)
    r.sendline(str(res))
r.interactive()