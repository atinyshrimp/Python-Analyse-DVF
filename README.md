# Analyse des Données DVF - Projet Immobilier

## Description du Projet

Ce dépôt contient le code et la documentation associés au projet d'analyse des données DVF (Demandes de Valeurs Foncières) concernant les transactions immobilières en France. L'objectif principal était d'analyser, nettoyer et visualiser ces données pour en extraire des informations pertinentes sur le marché immobilier.

## Contenu du Projet

- **Notebook d'Analyse :** Le fichier `Projet_Manon_Kevin_Joyce_v3.ipynb` est un notebook détaillé (format Jupyter Notebook) décrivant l'analyse effectuée, le nettoyage des données, les visualisations générées, ainsi qu'une analyse comparative avant et après la pandémie de COVID-19.
- **Application Web :** Le répertoire `mysite` comprend le code source de l'application web dynamique développée avec le framework Django. Cette application permet une exploration interactive des données immobilières analysées.

## Instructions d'Utilisation

### Dépendances

Les dépendances suivantes sont nécessaires pour exécuter le notebook d'analyse ainsi que l'application web :

- Python (version 3.9.18 ou supérieur)
- **Jupyter Notebook** ou **JupyterLab** (pour exécuter le notebook d'analyse)
- Pandas 
- Matplotlib
- Plotly
- Django

Copiez cette ligne de code pour tout installer dans votre environnement :
* PIP
```
pip install pandas matplotlib plotly Django
```
* Conda
```
conda install -c conda-forge pandas matplotlib plotly Django
```

### Notebook d'Analyse
1. Cloner ce dépôt : `git clone https://github.com/atinyshrimp/Python-Analyse-DVF.git`
2. Ouvrir le notebook `Analyse_DVF.ipynb` à l'aide de Jupyter Notebook ou JupyterLab.
3. Exécuter les cellules du notebook dans l'ordre pour visualiser l'analyse et les visualisations.

### Application Web
1. Assurez-vous d'avoir Python et Django installés localement.
2. Cloner ce dépôt : `git clone https://github.com/atinyshrimp/Python-Analyse-DVF.git`
3. Accéder au dossier `mysite`.
4. Exécuter `python manage.py runserver` pour lancer l'application localement.
5. Accéder à l'application via votre navigateur en utilisant l'URL donné.

## Auteurs

- [Manon](https://www.linkedin.com/in/manon-goffinet/)
- [Kevin](https://www.linkedin.com/in/kevin-hermand/)
- [Joyce](https://github.com/atinyshrimp)
