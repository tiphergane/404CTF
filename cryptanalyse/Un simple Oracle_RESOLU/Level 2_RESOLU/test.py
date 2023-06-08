#!/usr/bin/env python3

import pwn
import math
#pwn.context.log_level = "debug"

pattern = "404CTF{"
host, port = "challenges.404ctf.fr",31674
e = 65537

conn = pwn.remote(host,port)
conn.recvline()
conn.recvline()
C = int(conn.recvline().decode())
J =  str(C * pow(2,e)).encode()
conn.sendlineafter(b">", J)
conn.recvline()
data = int(conn.recvline().decode())
p = data // 2
M  = str(p.to_bytes((p.bit_length()+7)// 8, "big"))
if pattern in M:
    pwn.success("Flag is: {}".format(M))
else:
    print("prout")







