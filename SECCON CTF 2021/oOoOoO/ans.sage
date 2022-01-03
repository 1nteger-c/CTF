from Crypto.Util.number import *

M = 3358865267993523418646298427749210334190739093746169917905801902106704531466533019207168510725428625000745906615006168163760426165634422537200238665920036431174804069999894010449513018581107517
S = 81434408737825149523977840344877896815489474895176166647180625948548142497095545946587402230454660730614468241879031803665608158734074041583328238860751009218487635903923432583228418360634668
p = M

n = 128
N = ceil(sqrt(n) / 2)

base = b'\x4f' * 128
base = bytes_to_long(base) % p
s = S-base

a = []
for i in range(128):
    tmp = 0x20 << (i * 8)
    a.append(tmp % p)

b = []
for i in range(n):
    vec = [0 for _ in range(n + 1)]
    vec[i] = 1
    vec[-1] = N * a[i]
    b.append(vec)
    b.append([1 / 2 for _ in range(n)] + [N * s])

for k in range(128):
    print('time :',k)
    tmp = [1 / 2 for _ in range(n)] + [N * (s + p * k)]
    b[-1] = tmp

    BB = matrix(QQ, b)
    l_sol = BB.LLL()

    for e in l_sol:
        if e[-1] == 0:
            msg = 0
            isValidMsg = True
            for i in range(len(e) - 1):
                ei = 1 - (e[i] + (1 / 2))
                if ei != 1 and ei != 0:
                    isValidMsg = False
                    break

                msg |= int(ei) << i

            if isValidMsg:
                print('[*] Got flag:', long_to_bytes(msg))
                break
    if isValidMsg:
        break

a = bin(msg)[2:].rjust(128,'0')
print(a)
flag = b''

for i in range(len(a)):
    if a[i] == '0':
        flag += b'O'
    else:
        flag += b'o'
print(flag)

flag = bytes_to_long(flag)
if tmp % M == S:
    print((long_to_bytes(flag)))