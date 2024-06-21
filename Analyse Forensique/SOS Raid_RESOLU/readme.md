# SOS Raid 1 et 2

## SOS RAID 1 (1000 pts)

### Explications

Deux fichiers, un manuel, on sait que l'on nous demande de reconstruire des données, et dans le manuel on nous parle de RAID5 (parité), c'est parti !

### Premières constatations

En utilisant les outils habituel, nous nous appercevont vite que les fichiers ne sont pas de systèmes de fichier, et ils ne seront donc pas exploitable avec **mdadm** et **zfs**, il faut donc trouver autre chose.

Une autre information dans le manuel est super importante:

>>Type de RAID : 5
>>
>>Taille des blocs : **1 octet**
>>
>>https://fr.wikipedia.org/wiki/RAID_(informatique)#RAID_5_:_volume_agr%C3%A9g%C3%A9_par_bandes_%C3%A0_parit%C3%A9_r%C3%A9partie

La taille des blocs est de **1 octet** ce qui n'est pas standard dans la distribution d'un système de fichier normal.

En suivant les informations de la page wikipedia, on comprend que la parité est calculée de la façon suivante:

>>bloc1 XoR bloc2

ce qui donne en python:

```python
parite = bloc1^bloc2
```

Le bloc de parité va être distribué de façon logique sur les disques dans le schema suivant:

>>Nmax->Nmax-1->Nnax-2->Nmax-n

ou Nmax = le nombre max de dique dans le pool du raid, et Nmax-n = le nombre max moins le disque sur lequel nous sommes.

Il faut savoir que le raid5 est récupérable **SI ET SEULEMENT SI** nous ne perdons pas plus d'un disque, au dela les données ne sont plus récupérables.

Donc nous pouvons en déduire que notre array était de 3 disques, cela sera très important dans le reste de la procédure.

### Récupération du disk2.img

Afin de recréer le disque manquant, nous allons devoir lire les données bits par bits (taille de bloc, 1 octet).
Heureusement pour nous, Python le fait très bien:

```python3
#!/usr/bin/env python3

d1 = open("disk0.img","rb").read()
d2 = open("disk1.img","rb").read()
d3 = []

for i in range(len(c1)):
		d3 = open("disk2.img","wb").write(d1^d2)
        d3.close()

```

Super, nous avons récupéré le disque manquant, maintenant, il faut recréer ce qui est contenu dans la partion.

### Récupération du contenu

C'est n'est pas forcément plus compliqué, maintenant que nous avons nos trois disques, nous allons pouvoir, toujours via python, refaire ce qui est contenu.

```python3
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
```

On récupère la totalité des bytes des disques, on les stocks dans data.zip (petit raccourci sur le CTF, je connais déjà le format de sortie aujourd'hui) et ça devrait faire le café.

```zsh
Archive:  /media/RAID10/ctf/404CTF/2022/Analyse Forensique/SOS Raid_RESOLU/Level 1/data.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
       50  2022-05-16 12:32   flag.txt
    61863  2022-05-01 22:17   flag_c0rr_pt3d.png
---------                     -------
    61913                     2 files
```

Super, nous avons le flag pour le Level1 puis le flag du level2 qui sera un PNG a reconstruire il semblerait.

```
404CTF{RAID_5_3st_p4s_tr3s_c0mpl1qu3_1abe46685ecf}
```

Pour simplifier la récupération, nous pouvons automatiser les différentes action dans un script python unique

```python
#!/usr/bin/env python3

import pwn


def xorBytes(b0, b1):
    pwn.info("Recréation des données de l’array")
    data = ""
    b3 = bytearray(len(b0))
    for i in range(len(b0)):
        b0 = bytearray(b0)
        b1 = bytearray(b1)
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


def testDisk():
    pwn.info("Test de la reconstruction du disque manquant")
    if len("./disk0.img") == len("./disk2.img"):
        pwn.success("la reconstruction du disque a réussie")
    else:
        pwn.warn("ERREUR: la reconstruction à échoué, la taille des disques diffèrent")
        raise SystemExit()


def main():
    k = 1
    pwn.info("Reconstruction du RAID5")
    d0 = open("disk0.img", "rb")
    d1 = open("disk1.img", "rb")
    data = xorBytes(d0.read(), d1.read())
    write = writeFile(data)
    d2 = open("disk2.img", "rb")
    d0.close()
    d1.close()
    d2.close()
    testDisk()
    extractData(k)


if __name__ == "__main__":
    main()
```

## SOS RAID 2
