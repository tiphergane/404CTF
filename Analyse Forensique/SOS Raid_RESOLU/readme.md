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

```
