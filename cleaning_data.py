# -*- coding: utf-8 -*-
"""
Created on Tue May 16 19:52:54 2023

@author: Joyce
"""

import pandas as pd

#%% Chargement des données
foncier2019 = pd.read_csv(r"C:\Users\Joyce\OneDrive - De Vinci\A3\S6\Informatique\Langage Python\Projet\Data\valeursfoncieres-2019.txt",
                       low_memory=False, sep="|")

foncier2022 = pd.read_csv(r"C:\Users\Joyce\OneDrive - De Vinci\A3\S6\Informatique\Langage Python\Projet\Data\valeursfoncieres-2022.txt",
                       low_memory=False, sep="|")

datasets=[foncier2019, foncier2022]

#%% Fonction pour les codes région
def CodeRegion(codeDep):
    if codeDep=="01" or codeDep=="03" or codeDep=="07" or codeDep=="15" or codeDep=="26" or codeDep=="38" or codeDep=="42" or codeDep=="43" or codeDep=="63" or codeDep=="69" or codeDep=="73" or codeDep=="74":
        return "84"
    elif codeDep=="02" or codeDep=="59" or codeDep=="60" or codeDep=="62" or codeDep=="80":
        return "32"
    elif codeDep=="04" or codeDep=="05" or codeDep=="06" or codeDep=="13" or codeDep=="83" or codeDep=="84":
        return "93"
    elif codeDep=="08" or codeDep=="10" or codeDep=="51" or codeDep=="52" or codeDep=="54" or codeDep=="55" or codeDep=="57" or codeDep=="67" or codeDep=="68" or codeDep=="88":
        return "44"
    elif codeDep=="09" or codeDep=="11" or codeDep=="12" or codeDep=="30" or codeDep=="31" or codeDep=="32" or codeDep=="34" or codeDep=="46" or codeDep=="48" or codeDep=="65" or codeDep=="66" or codeDep=="81" or codeDep=="82":
        return "76"
    elif codeDep=="14" or codeDep=="27" or codeDep=="50" or codeDep=="61" or codeDep=="76" or codeDep=="14":
        return "28"
    elif codeDep=="16" or codeDep=="17" or codeDep=="17" or codeDep=="19" or codeDep=="23" or codeDep=="24" or codeDep=="33" or codeDep=="40" or codeDep=="47" or codeDep=="64" or codeDep=="79" or codeDep=="86" or codeDep=="87":
        return "75"
    elif codeDep=="18" or codeDep=="28" or codeDep=="36" or codeDep=="37" or codeDep=="41" or codeDep=="45":
        return "24"
    elif codeDep=="2A" or codeDep=="2B":
        return "94"
    elif codeDep=="21" or codeDep=="25" or codeDep=="39" or codeDep=="58" or codeDep=="70" or codeDep=="71" or codeDep=="89" or codeDep=="90":
        return "27"
    elif codeDep=="22" or codeDep=="29" or codeDep=="35" or codeDep=="56":
        return "53"
    elif codeDep=="44" or codeDep=="49" or codeDep=="53" or codeDep=="72" or codeDep=="85":
        return "52"
    elif codeDep=="75" or codeDep=="77" or codeDep=="78" or codeDep=="91" or codeDep=="92" or codeDep=="93" or codeDep=="94" or codeDep=="95":
        return "11"
    elif codeDep=="971":
        return "01"
    elif codeDep=="972":
        return "02"
    elif codeDep=="973":
        return "03"
    elif codeDep=="974":
        return "04"

#%% Nettoyage des données
for i in range(len(datasets)):
    df=datasets[i]
    
    # Suppression des colonnes "inutiles"
    df = df.drop(['Identifiant de document', '1 Articles CGI', 
                   '2 Articles CGI', '3 Articles CGI', '4 Articles CGI', 
                   '5 Articles CGI', 'Reference document', 'No disposition', 
                   'No voie', 'B/T/Q', 'Code voie', 'Prefixe de section', 
                   'Section', 'No plan', 'No Volume', '1er lot', 
                   'Surface Carrez du 1er lot', '2eme lot', 
                   'Surface Carrez du 2eme lot', '3eme lot', 
                   'Surface Carrez du 3eme lot', '4eme lot', 
                   'Surface Carrez du 4eme lot', '5eme lot', 
                   'Surface Carrez du 5eme lot', 'Code type local', 
                   'Identifiant local', 'Nature culture', 
                   'Nature culture speciale'], axis=1)

    # Suppression des lignes contenant des valeurs nulles (non exploitables)
    df = df.dropna()

    # Conversion des colonnes en leur type de données approprié
    df['Date mutation'] = pd.to_datetime(df['Date mutation'], format='%d/%m/%Y')
    df['Valeur fonciere'] = pd.to_numeric(df['Valeur fonciere'].str.replace(',', '.'))
    df['Surface reelle bati'] = df['Surface reelle bati'].astype('int')
    df['Nombre pieces principales'] = df['Nombre pieces principales'].astype('int')
    df['Surface terrain'] = df['Surface terrain'].astype('int')
    df['Code departement'] = df['Code departement'].astype(str)
    df['Code région']=df['Code departement'].apply(CodeRegion)
    
    df=df.dropna(axis=0,subset=['Valeur fonciere','Surface terrain'])
    df=df[df['Surface terrain'] != 0]

    # Ajouter une colonne 'Mois' au DataFrame
    df['Mois'] = df['Date mutation'].dt.month
    
    # Créer une nouvelle colonne 'Prix par mètre carré'
    df['Prix par mètre carré'] = df['Valeur fonciere'] / df['Surface terrain']

    # Correction du format des codes postaux 
    df["Code postal"] = df["Code postal"].apply(lambda x: "0" + str(x).split('.')[0] if len(str(x).split('.')[0]) == 4 else str(x).split('.')[0])


    datasets[i] = df
    
foncier2019 = datasets[0]
foncier2022 = datasets[1]

#%% Ecriture des datasets dans un fichier .csv
foncier2019.to_csv(r"C:\Users\Joyce\OneDrive - De Vinci\A3\S6\Informatique\Langage Python\Projet\Data\foncier2019_cleaned.csv")
foncier2022.to_csv(r"C:\Users\Joyce\OneDrive - De Vinci\A3\S6\Informatique\Langage Python\Projet\Data\foncier2022_cleaned.csv")