#!/usr/bin/env python3

import pwn


def xorBytes(b0, b1):
    pwn.info("Calcul des sommes de contrôle")
    b3 = bytearray(len(b0))
    b0 = bytearray(b0)
    b1 = bytearray(b1)
    for i in range(len(b0)):
        b3[i] = b0[i] ^ b1[i]
    return b3


def writeFile(data):
    pwn.info("reconstruction du disque")
    d2 = open("disk2.img", "wb")
    d2.write(data)
    d2.close()


def extractData(size):
    pwn.info("la taille est de: {} octet".format(size))
    d1 = open("disk0.img", "rb")
    d2 = open("disk1.img", "rb")
    d3 = open("disk2.img", "rb")
    x = 2
    n = 27756
    data = open("data.zip", "wb")
    pwn.info("extraction des données")
    for _ in range(n):
        blocks = (d1.read(size), d2.read(size), d3.read(size))
        data_blocks = [b for i, b in enumerate(blocks) if i != x]
        x = (x - 1) % 3
        data.write(b"".join(data_blocks))
    d1.close()
    d2.close()
    d3.close()


def testDisk():
    pwn.info("Test de la reconstruction du disque manquant")
    if len("./disk0.img") == len("./disk2.img"):
        pwn.success("la reconstruction du disque a réussie")
    else:
        pwn.warn("ERREUR: la reconstruction à échoué, la taille des disques diffèrent")
        raise SystemExit()


def main():
    k = 1
    pwn.warn("Reconstruction du RAID5")
    d0 = open("disk0.img", "rb")
    d1 = open("disk1.img", "rb")
    data = xorBytes(d0.read(), d1.read())
    writeFile(data)
    testDisk()
    extractData(k)


if __name__ == "__main__":
    main()
