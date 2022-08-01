from pwn import *
r = process(['python3','server.py'])
r.recvline()
data = []
for i in range(9):
    data.append(eval(r.recvline()))

unknown_idx = 55
for i in range(9):
    unknown_idx= unknown_idx - data[i][0]

assert unknown_idx > 1 
print('unknown_idx : ',unknown_idx)
for unknown in range(100000):
    if unknown % 1000 == 0:
        print(f'checking : {unknown}')
    # print(unknown)
    secret = 0
    M = Matrix(ZZ, 9)
    A = Matrix(ZZ, 9, 1)

    for i in range(9):
        for j in range(9):
            M[i,j] = data[i][0] ** (data[j][0] - 1)
        A[i,0] = data[i][1] - unknown * data[i][0] ** (unknown_idx -1)

    B = M.inverse()* A
    check = False
    for i in range(9):
        tmp = B[i,0]
        if (tmp - int(tmp) != 0):
            check = True
            break
        if tmp < 0 or tmp > 500000:
            check = True
            break
    if check:
        continue
    secret = B[0,0]
    break


r.recvuntil('Enter my secret: ')
log.info("secret :  " + str(secret))
r.sendline(str(secret).encode())
r.interactive()