#!/usr/bin/env python3

import pwn
import math
#pwn.context.log_level = "debug"

pattern = "404CTF{"
host, port = "challenge.404ctf.fr",32128
e = 65537

conn = pwn.remote(host,port)
conn.recvline()
C = int(conn.recvline().decode())
conn.recvline()
N = int(conn.recvline().decode().split(" ")[2])
J =  str(C * pow(2,e,N) % N).encode()
conn.sendlineafter(">", J)
conn.recvline()
data = int(conn.recvline().decode())
p = data // 2
M  = str(p.to_bytes((p.bit_length()+7)// 8, "big"))
if pattern in M:
    print(M)
else:
    print("prout")







