import string
import math
import struct
import hashlib
from pwn import *
from multiprocessing import Pool, cpu_count, Queue
from Crypto.Util.number import bytes_to_long
from itertools import permutations


class Realxorshift:
    def __init__(self, a, b):
        self.state = [a, b]
        self.cache = []

    def xs128p(self):
        s1 = self.state[0] & 0xFFFFFFFFFFFFFFFF
        s0 = self.state[1] & 0xFFFFFFFFFFFFFFFF
        s1 ^= (s1 << 23) & 0xFFFFFFFFFFFFFFFF
        s1 ^= (s1 >> 17) & 0xFFFFFFFFFFFFFFFF
        s1 ^= s0 & 0xFFFFFFFFFFFFFFFF
        s1 ^= (s0 >> 26) & 0xFFFFFFFFFFFFFFFF
        self.state[0] = self.state[1] & 0xFFFFFFFFFFFFFFFF
        self.state[1] = s1 & 0xFFFFFFFFFFFFFFFF
        generated = self.state[0] & 0xFFFFFFFFFFFFFFFF
        return generated

    def getRandom(self):
        if self.cache == []:
            for i in range(64):
                self.cache.append(to_double(self.xs128p()))
            self.cache = self.cache[::-1]
        ret = self.cache[0]
        self.cache = self.cache[1:]
        return ret


class xorshift:
    def __init__(self):
        self.state = [[(1 << (64 * i + (63 - j)))
                       for j in range(64)] for i in range(2)]

    def _xor(self, a, b):
        return [x ^ y for x, y in zip(a, b)]

    def _and(self, a, x):
        return [v if (x >> (31 - i)) & 1 else 0 for i, v in enumerate(a)]

    def _shiftr(self, a, x):
        return [0] * x + a[:-x]

    def _shiftl(self, a, x):
        return a[x:] + [0] * x

    def xs128p(self):
        s1 = self.state[0]
        s0 = self.state[1]
        s1 = self._xor(s1, self._shiftl(s1, 23))
        s1 = self._xor(s1, self._shiftr(s1, 17))
        s1 = self._xor(s1, s0)
        s1 = self._xor(s1, self._shiftr(s0, 26))
        self.state[0] = self.state[1]
        self.state[1] = s1
        generated = self.state[0]
        return generated

    def getRandom(self):
        return self.xs128p()


class Solver:
    def __init__(self):
        self.equations = []
        self.outputs = []

    def insert(self, equation, output):
        for eq, o in zip(self.equations, self.outputs):
            lsb = eq & -eq
            if equation & lsb:
                equation ^= eq
                output ^= o

        if equation == 0:
            return

        lsb = equation & -equation
        for i in range(len(self.equations)):
            if self.equations[i] & lsb:
                self.equations[i] ^= equation
                self.outputs[i] ^= output

        self.equations.append(equation)
        self.outputs.append(output)

    def solve(self):
        num = 0
        for i, eq in enumerate(self.equations):
            if self.outputs[i]:
                num |= eq & -eq
        state = [(num >> (64 * i)) & 0xFFFFFFFFFFFFFFFF for i in range(2)]
        return state


def to_double(value):
    double_bits = (value >> 12) | 0x3FF0000000000000
    return struct.unpack('d', struct.pack('<Q', double_bits))[0] - 1


pq = Queue()
ncpu = max(cpu_count() - 2, 1)


def solve_pow(i, goal):
    global pq
    v = list(string.ascii_letters + string.digits)
    for _ in range(i):
        random.shuffle(v)
    for s in permutations(v, 8):
        a = bytes_to_long(hashlib.sha256(
            goal + ''.join(s).encode('utf-8')).digest()) & 0xffffff
        if a == 0xffffff:
            pq.put(goal + ''.join(s).encode('utf-8'))
            return


def compute(rl, rr):
    global pq
    for warmup_len in range(rl, rr):
        xorShift = xorshift()
        equations = [xorShift.getRandom() for _ in range(256)]
        prefixs = [-1] * warmup_len + prefix + [-1] * (256-prefix_len-warmup_len)
        outputs = []
        for i in range(0, 256, 64):
            outputs += prefixs[i:i+64][::-1]
        solver = Solver()
        out = [0b000, 0b00, 0b001, 0b0, 0b01, 0b011, -
               1, 0b100, 0b10, 0b1, 0b110, 0b11, 0b111]
        bit = [3, 2, 3, 1, 2, 3, 0, 3, 2, 1, 3, 2, 3]
        for i in range(len(outputs)):
            if outputs[i] == -1:
                continue
            for j in range(bit[outputs[i]]):
                solver.insert(
                    equations[i][j], (out[outputs[i]] >> (bit[outputs[i]] - 1 - j)) & 1)

        state0, state1 = solver.solve()
        rand = Realxorshift(state0, state1)

        output = ''
        for i in range(warmup_len):
            rand.getRandom()

        for i in range(prefix_len+128):
            output += alphabet[math.floor(len(alphabet) * rand.getRandom())]

        expected = output[prefix_len:]

        hashCalc = hashlib.md5(expected.encode()).hexdigest()
        if hashCalc == hashVal:
            pq.put(expected)
            return 0


r = process(['python3', 'server.py'])
# r = remote('fastrology.chal.pwni.ng', 1337)

if r.recv(1) == b'G':
    r.recvuntil(b'ive me a string starting with ')
    goal = r.recv(10)
    log.info(f'pow : {goal}')
    with Pool(ncpu) as pl:
        ar = pl.starmap_async(solve_pow, [(i, goal) for i in range(ncpu)])
        res = pq.get()
        pl.terminate()

    log.info(f'pow result : {res}')
    r.sendline(res)
    r.recvline()

### CHALL  START ###

alphabet = '♈♉♊♋♌♍♎♏♐♑♒♓⛎'


def alp_to_idx(alp):
    return alphabet.index(alp)


def idx_to_alp(idx):
    return alphabet[idx]

prefix_len = 192
chall = b'new moon'
r.recvuntil(chall)
r.sendline(chall)

for round in range(50):
    r.recvuntil(chall)
    sleep(0.5)
    print(f'[+] ROUND : {round+1} / 50')
    r.recvline()

    prefix_recv = r.recvline()[:-1].decode()
    assert len(prefix_recv) == prefix_len
    prefix = [alp_to_idx(x) for x in prefix_recv]
    hashVal = r.recvline()[:-1].decode()
    pq = Queue()
    with Pool(ncpu) as pl:
        ar = pl.starmap_async(
            compute, [(64 * i // ncpu, 64 * (i+1) // ncpu) for i in range(ncpu)])
        expectedAnswer = pq.get(timeout=15)
        pl.terminate()
    ## Data receive done ##
    r.sendline(expectedAnswer.encode())
r.interactive()
