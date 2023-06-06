# PING  PONG

```
 Ping Pong
983

Nous avons repéré une communication bizarre provenant des serveurs de Hallebarde. On soupçonne qu'ils en aient profité pour s'échanger des informations vitales. Pouvez-vous investiguer ?
```


## Analyse

Dans wireshark, nous allons regarder ce qui ce trame (petite blague), nous avons uniquement des paquets ICMP, mon premier reflexe est de regarder ce qu'il y a dans la section data.

Malheureusement c'est un mauvais choix, après une analyse un peu plus  poussée, la partie ~~Lenght~~ me semble étrange, et les 3 premiers paquets me font penser au flag __404CTF__
(94,90,94), en regardant les 3 suivants, l'écart est le bon dans l'ordre alphabetique, mais ce n'est ni de l'hexadécimal (4 = 0x34) ni du decimal (4 = 52), un peu plus de neurones et
la solution s'offre à nous, il faut retirer __42__  au nombres trouvé. Un petit script python nous simplifiera la solution.

## Script

```python3
#!/usr/bin/env python3

import pwn

liste = [94,90,94,109,126,112,165,127,152,137,154,91,152,145,137,154,90,152,145,137,154,94,157,137,157,147,137,91,152,152,90,141,93,152,158,167]
pattern = "404CTF"

def working():
    chaine = ""
    for c in liste:
        chaine += chr(c - 42)
    if pattern in chaine:
        pwn.success("le flag est : {}".format(chaine))

    else:
        pwn.warn("OH NONONONONONONONONO")


if __name__ == "__main__":
    working() 
```

le résultat du script:

```bash
[+] le flag est : 404CTF{Un_p1ng_p0ng_p4s_si_1nn0c3nt}
```

## Nouvelle version du script

Car on apprend toujours avec le temps et les autres CTF, et que cela faisait un petit moment que je voulais jouer avec Scapy, voici la version full auto

```python3
#!/usr/bin/env python3

import pwn
import scapy.all

pcap = scapy.all.rdpcap("ping.pcapng")
answer = ""
j = 0

pwn.info(f"PCAP contains {str(pcap)!r}")

for i in range(len(pcap)):
    if i % 2 == 0:
        if pcap[i].haslayer(scapy.all.ICMP):
            print(f"temp flag is {answer}", end="\r")
            answer += str(chr(int(len(pcap[i]) - 42)))
pwn.success(f"flag is : {answer}")
```
