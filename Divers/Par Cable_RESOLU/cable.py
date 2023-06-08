#!/usr/bin/env python3

import pwn

liste = open("cable.txt", "r").read().split()

data = ""
flag = ""
pattern = "404CTF{"
b1 = ""
b2 = ""

for i in range(len(liste)-1):
    b1 = liste[i]
    b2 = liste[i+1]
    i += 2
    if b1 == b2:
        data += "0"
    else:
        data += "1"

pwn.info("chaine à décoder: {}".format(data))
""" Écriture de data dans un fichier
binaire = open("binaire.txt", "w")
binaire.write(data)
binaire.close()
"""
n = int(data,2)
try:
    flag = n.to_bytes((n.bit_length() +7) //8, "big").decode()
except:
    flag = "gniagniagnia"

if pattern in flag:
    pwn.success("flag is : {}".format(flag))
else:
    pwn.warn("Oh no ! no flag here")
