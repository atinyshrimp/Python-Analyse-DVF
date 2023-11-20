# Data à télécharger
Le dossier de data est malheureusement trop volumineux pour le push sur GitHub. Mais, heureusement, les données sont disponibles en open source [ici](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/).\
\
Il faut télécharger les fichiers contenant les données suivantes :
* Valeurs foncières 2019
* Valeurs foncières 2020
* Valeurs foncières 2021
* Valeurs foncières 2022

Finalement, pour obtenir les données nettoyées, il faut se placer dans le dossier parent et lancer `cleaning_data.py`.\
```
python cleaning_data.py
```
\
Normalement, le dossier "Data" sera donc mis en place !