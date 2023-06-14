from GF import GF
from constants import Rcon
import os

get_inv = [0, 1, 141, 246, 203, 82, 123, 209, 232, 79, 41, 192, 176, 225, 229, 199, 116, 180, 170, 75, 153, 43, 96, 95, 88, 63, 253, 204, 255, 64, 238, 178, 58, 110, 90, 241, 85, 77, 168, 201, 193, 10, 152, 21, 48, 68, 162, 194, 44, 69, 146, 108, 
243, 57, 102, 66, 242, 53, 32, 111, 119, 187, 89, 25, 29, 254, 55, 103, 45, 49, 245, 105, 167, 100, 171, 19, 84, 37, 233, 9, 237, 92, 5, 202, 76, 36, 135, 191, 24, 62, 34, 240, 81, 236, 97, 23, 22, 94, 175, 211, 73, 166, 54, 67, 244, 71, 145, 223, 51, 147, 33, 59, 121, 183, 151, 133, 16, 181, 186, 60, 182, 112, 208, 6, 161, 250, 129, 130, 131, 126, 127, 128, 150, 115, 190, 86, 155, 158, 149, 217, 247, 2, 185, 164, 222, 106, 50, 109, 216, 138, 132, 114, 42, 20, 159, 136, 249, 220, 137, 154, 251, 124, 46, 195, 143, 184, 101, 72, 38, 200, 18, 74, 206, 231, 210, 98, 12, 224, 31, 239, 17, 117, 120, 113, 165, 142, 118, 61, 189, 188, 134, 87, 11, 40, 47, 163, 218, 212, 228, 15, 169, 39, 83, 4, 27, 252, 172, 230, 122, 7, 174, 99, 197, 219, 226, 234, 148, 139, 196, 213, 157, 248, 144, 107, 177, 13, 214, 235, 198, 14, 207, 173, 8, 78, 215, 227, 93, 80, 30, 179, 91, 35, 56, 52, 104, 70, 3, 140, 221, 156, 125, 160, 205, 26, 65, 28]
s_box_inv = [82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]

def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] = state[i][j] + round_key[i][j]

def add_round_key_inv(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] = state[i][j] + round_key[i][j]

def shift_rows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]

def shift_rows_inv(state):
    state[1][1], state[1][2], state[1][3], state[1][0] = state[1][0], state[1][1], state[1][2], state[1][3]
    state[2][2], state[2][3], state[2][0], state[2][1] = state[2][0], state[2][1], state[2][2], state[2][3]
    state[3][3], state[3][0], state[3][1], state[3][2] = state[3][0], state[3][1], state[3][2], state[3][3]

def mix_columns(state):
    mat = [[GF(2), GF(3), GF(1), GF(1)],
           [GF(1), GF(2), GF(3), GF(1)],
           [GF(1), GF(1), GF(2), GF(3)],
           [GF(3), GF(1), GF(1), GF(2)]]
    tmp = [GF(0) for _ in range(4)]
    for j in range(4):
        for i in range(4):
            tmp[i] = mat[i][0] * state[0][j] + mat[i][1] * state[1][j] + mat[i][2] * state[2][j] + mat[i][3] * state[3][j]
        for i in range(4):
            state[i][j] = tmp[i]

def mix_columns_inv(state):
    mat = [[GF(14), GF(11), GF(13), GF(9)],
           [GF(9), GF(14), GF(11), GF(13)],
           [GF(13), GF(9), GF(14), GF(11)],
           [GF(11), GF(13), GF(9), GF(14)]]
    tmp = [GF(0) for _ in range(4)]
    for j in range(4):
        for i in range(4):
            tmp[i] = mat[i][0] * state[0][j] + mat[i][1] * state[1][j] + mat[i][2] * state[2][j] + mat[i][3] * state[3][j]
        for i in range(4):
            state[i][j] = tmp[i]

def get_sbox_and_verify(x):
    xinv = get_inv[x.val]
    xinv = GF(xinv)
    assert x * (x * xinv - GF(1)) == GF(0)
    return xinv + xinv.lrotate(1) + xinv.lrotate(2) + xinv.lrotate(3) + xinv.lrotate(4) + GF(99)

def key_schedule(round_keys, KEY):
    for i in range(4):
        for j in range(4):
            round_keys[i][j].val = KEY[i + 4*j]


    for i in range(4, 4*ROUNDS+4):
        if i % 4 == 0:
            round_keys[0][i] = round_keys[0][i-4] \
                            + get_sbox_and_verify(round_keys[1][i-1]) \
                            + GF(Rcon[i // 4])

            for j in range(1, 4):
                round_keys[j][i] = round_keys[j][i-4] \
                                + get_sbox_and_verify(round_keys[(j+1)%4][i-1])
        
        else:
            for j in range(4):
                round_keys[j][i] = round_keys[j][i-4] + round_keys[j][i-1]


def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = get_sbox_and_verify(state[i][j])

def sub_bytes_inv(state):
    for i in range(4):
        for j in range(4):
            state[i][j].val = s_box_inv[state[i][j].val]


## START
from pwn import *
r = process(['python3', 'prob.py'])
r.recvuntil(b'Your goal is to find KEY K which satisfies AES_K(')
PLAINTEXT = bytes.fromhex(r.recvuntil(b')')[:-1].decode())
r.recvuntil(b' = ')
CIPHERTEXT = bytes.fromhex(r.recvline()[:-1].decode())
r.recvuntil(b'KEY > ')
r.sendline(PLAINTEXT.hex().encode())


KEY = PLAINTEXT

ROUNDS = 10
round_keys = [[GF(0) for i in range(4 * (ROUNDS + 1))] for j in range(4)]

key_schedule(round_keys, KEY)
state = [[GF(0) for i in range(4)] for j in range(4)]
for i in range(4):
    for j in range(4):
        state[i][j].val = CIPHERTEXT[i + 4*j]

add_round_key_inv(state, [[round_keys[z][j] for j in range(4*ROUNDS, 4*ROUNDS+4)] for z in range(4)])
shift_rows_inv(state)
sub_bytes_inv(state)

for i in range(ROUNDS - 2, -1, -1):
    add_round_key_inv(state, [[round_keys[z][j] for j in range(4*i+4, 4*i+8)] for z in range(4)])
    mix_columns_inv(state)
    shift_rows_inv(state)
    if i == 0:
        break
    sub_bytes_inv(state)

for i in range(4, 4*ROUNDS+4):
    r.recvuntil(b'inv(').decode()
    num = int(r.recvuntil(b')')[:-1],16)
    r.sendlineafter(b' > ', hex(get_inv[num]).encode())

array = [5, 79, 145, 219, 44, 102, 184, 242, 87, 29, 195, 137, 126, 52, 234, 160, 161, 235, 53, 127, 136, 194, 28, 86, 243, 185, 103, 45, 218, 144, 78, 4, 76, 6, 216, 146, 101, 47, 241, 187, 30, 84, 138, 192, 55, 125, 163, 233, 232, 162, 124, 54, 193, 139, 85, 31, 186, 240, 46, 100, 147, 217, 7, 77, 151, 221, 3, 73, 190, 244, 42, 96, 197, 143, 81, 27, 236, 166, 120, 50, 51, 121, 167, 237, 26, 80, 142, 196, 97, 43, 245, 191, 72, 2, 220, 150, 222, 148, 74, 0, 247, 189, 99, 41, 140, 198, 24, 82, 165, 239, 49, 123, 122, 48, 238, 164, 83, 25, 199, 141, 40, 98, 188, 246, 1, 75, 149, 223, 32, 106, 180, 254, 9, 67, 157, 215, 114, 56, 230, 172, 91, 17, 207, 133, 132, 206, 16, 90, 173, 231, 57, 115, 214, 156, 66, 8, 255, 181, 107, 33, 105, 35, 253, 183, 64, 10, 212, 158, 59, 113, 175, 229, 
18, 88, 134, 204, 205, 135, 89, 19, 228, 174, 112, 58, 159, 213, 11, 65, 182, 252, 34, 104, 178, 248, 38, 108, 155, 209, 15, 69, 224, 170, 116, 62, 201, 131, 93, 23, 22, 92, 130, 200, 63, 117, 171, 225, 68, 14, 208, 154, 109, 39, 249, 179, 251, 177, 111, 37, 210, 152, 70, 12, 169, 227, 61, 119, 128, 202, 20, 94, 95, 21, 203, 129, 118, 60, 226, 168, 13, 71, 153, 211, 36, 110, 176, 250]
for i in range(4):
    for j in range(4):
        r.sendlineafter(b'inv(00) > ', hex(array[state[i][j].val]).encode())

for i in range(16 * (ROUNDS - 1)):
    r.recvuntil(b'inv(').decode()
    num = int(r.recvuntil(b')')[:-1],16)
    r.sendlineafter(b' > ', hex(get_inv[num]).encode())

r.interactive()