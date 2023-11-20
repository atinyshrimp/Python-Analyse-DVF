from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import pandas as pd
import plotly.express as px

from urllib.request import urlopen
import json
with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
    departement = json.load(response)



def index(request):    
    template = loader.get_template('template0.html')
    context = { 
        }
    
    return HttpResponse(template.render(context, request))


def index1(request):    
    template1 = loader.get_template('template1.html')
    context = { 
        }
    
    return HttpResponse(template1.render(context, request))


def evolution_ventes(df, annee):
    # Ajouter une colonne 'Mois' au DataFrame
    df['Mois'] = df['Date mutation'].dt.month

    # Compter le nombre de ventes par mois
    ventes_par_mois = df.groupby('Mois')['Date mutation'].count().reset_index()

    # Créer un graphique d'évolution des ventes selon les mois avec Plotly Express
    fig = px.line(ventes_par_mois, x='Mois', y='Date mutation')

    fig.update_layout(
        title=f"Évolution des ventes selon les mois en {annee}",
        xaxis_title="Mois",
        yaxis_title="Nombre de ventes",
        xaxis=dict(tickmode='linear'),
        yaxis=dict(gridcolor='lightgray'),
    )

    plot_html = fig.to_html(full_html=False, default_height=500, default_width=1100)
    return(plot_html)


def map_valeur_fonciere(df):
    # VALEUR FONCIERE MOYENNE PAR DEPARTEMENT
    # Calcul de la valeur fonciere moyenne par departement
    df['Valeur fonciere']=df['Valeur fonciere'].replace(',','.',regex=True).astype(float)
    d=pd.DataFrame(df.groupby(df["Code departement"]),df.groupby(df["Code departement"]).mean()["Valeur fonciere"])

    dep_vf=d.reset_index()
    dep_vf=dep_vf.rename(columns={0 : "Département"})
    dep_vf=dep_vf.drop(columns=[1])

    dep_vf.sort_values(by=['Valeur fonciere'], inplace=True, ascending=False)

    dep_vf=dep_vf.reset_index()


    #Affichage de la carte
    fig = px.choropleth_mapbox(dep_vf, geojson=departement, locations='Département', color='Valeur fonciere',
                            color_continuous_scale="Viridis",
                            range_color=(0,1000000),  # ajustez cette plage en fonction de la plage de vos données
                            mapbox_style='carto-positron',
                            featureidkey="properties.code",
                            zoom=4,
                            center={'lat': 47, 'lon': 2},
                            opacity=0.8,)
    fig.update_layout(title=f"Valeurs foncières par département en 2022")
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=1100)
    return(plot_html)


def map_ventes_departement(df):
    ventes_par_departement_2022 = df.groupby("Code departement").size().reset_index(name="Nombre de ventes")

    fig = px.choropleth_mapbox(ventes_par_departement_2022, geojson=departement,
        locations="Code departement",
        color="Nombre de ventes",
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        featureidkey="properties.code",
        center={"lat": 46.603354, "lon": 1.888334},
        zoom=4,
        opacity=0.8,
        labels={"Nombre de ventes": "Nombre de ventes"})

    fig.update_layout(title="Répartition des ventes en France en 2022")
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=1100)
    return(plot_html)


def map_ventes_idf(df):
    # Répartition géographique des ventes en Île-de-France en 2022
    idf_data_2022 = df[df['Code région']=='11']
    ventes_departement_2022 = idf_data_2022['Code departement'].value_counts()

    fig = px.choropleth(ventes_departement_2022, geojson=departement, locations=ventes_departement_2022.index,
                    color=ventes_departement_2022.values, featureidkey='properties.code',
                    projection="mercator", color_continuous_scale="Viridis",
                    labels={'color': 'Nombre de ventes'},
                    title='Répartition géographique des ventes en Île-de-France en 2022')
    fig.update_geos(fitbounds="locations", visible=False)
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=1100)
    return(plot_html)


def prix_m2(df):
    # Filtrer les données pour ne conserver que les ventes
    ventes = df[df['Nature mutation'] == 'Vente']

    # Définir une fonction pour supprimer les valeurs aberrantes dans un DataFrame
    def remove_outliers(df):
        Q1 = df['Prix par mètre carré'].quantile(0.25)
        Q3 = df['Prix par mètre carré'].quantile(0.75)
        IQR = Q3 - Q1
        df_out = df[~((df['Prix par mètre carré'] < (Q1 - 0.9 * IQR)) | (df['Prix par mètre carré'] > (Q3 + 0.9 * IQR)))]
        return df_out
    
    ventes = ventes.groupby('Code departement').apply(remove_outliers).reset_index(drop=True)
    prix_moyen_par_departement = ventes.groupby('Code departement')['Prix par mètre carré'].mean().reset_index()
    prix_moyen_par_departement.sort_values(by=['Prix par mètre carré'], inplace=True, ascending=False)
    labels = prix_moyen_par_departement["Code departement"]
    values = prix_moyen_par_departement["Prix par mètre carré"]

    fig = px.bar(x=labels, y=values, labels={'x':'Département', 'y':'Prix au m²'}, title='Comparaison du prix du m² (en 2022)')
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=1100)
    return(plot_html)


def prix_m2_en_france(df):
    # Filtrer les données pour ne conserver que les ventes et créer une copie explicite
    ventes = df[df['Nature mutation'] == 'Vente'].copy()

    # Calculer la surface totale en utilisant la colonne 'Surface reelle bati'
    ventes['Surface totale'] = ventes['Surface reelle bati']

    # Filtrer les données pour éliminer les lignes où la surface totale est égale à zéro ou très proche de zéro
    ventes = ventes[ventes['Surface totale'] > 0.0]

    # Créer une nouvelle colonne 'Prix par mètre carré'
    ventes['Prix par mètre carré'] = ventes['Valeur fonciere'] / ventes['Surface totale']

    # Calculer le premier et troisième quartile (Q1 et Q3) ainsi que l'IQR
    Q1 = ventes['Prix par mètre carré'].quantile(0.25)
    Q3 = ventes['Prix par mètre carré'].quantile(0.75)
    IQR = Q3 - Q1

    # Filtrer les données pour éliminer les valeurs aberrantes en utilisant l'IQR
    ventes_iqr = ventes[(ventes['Prix par mètre carré'] >= Q1 - 1.5 * IQR) & (ventes['Prix par mètre carré'] <= Q3 + 1.5 * IQR)]

    # Créer un diagramme en boîte à moustaches du prix par mètre carré avec Plotly Express
    fig = px.box(ventes_iqr, y='Prix par mètre carré', title='Diagramme en boîte à moustaches du prix par m² en France en 2022')
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=1100)
    return(plot_html)


def surface_nb_pieces(df):
    ventes = df[df['Nature mutation'] == 'Vente']
    df_nb_piece = ventes.groupby(['Nombre pieces principales']).mean()
    df_nb_piece = df_nb_piece.reset_index()

    fig = px.scatter(df_nb_piece, x="Nombre pieces principales", y="Surface terrain")

    fig.update_layout(
        title="Relation entre le nombre de pièces principales et la surface terrain (en 2022)",
        xaxis_title="Nombre de pièces principales",
        yaxis_title="Surface terrain",
        showlegend=False
    )
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=1100)
    return(plot_html)


def types_biens(df, annee):
    types_biens = df['Type local'].value_counts(normalize=True)*100
    fig = px.pie(types_biens, values=types_biens.values, names=types_biens.index, title=f'Types de biens en {annee}')
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=1100)
    return(plot_html)


def index2(request):

    template1 = loader.get_template('template1.html')
    foncier2019 = pd.read_csv("../Data/foncier2019_cleaned.csv", low_memory=False, sep=",")
    foncier2019['Date mutation'] = pd.to_datetime(foncier2019['Date mutation'], format='%Y-%m-%d')
    foncier2019=foncier2019.dropna(axis=1,thresh=500000)
    foncier2019=foncier2019.drop_duplicates()

    foncier2022 = pd.read_csv("../Data/foncier2022_cleaned.csv", low_memory=False, sep=",")
    foncier2022['Date mutation'] = pd.to_datetime(foncier2022['Date mutation'], format='%Y-%m-%d')

    if (request.GET['model']=="Evolution_des_ventes"):
        plot_html=evolution_ventes(foncier2019, 2019)
        plot_html2=evolution_ventes(foncier2022, 2022)
        context = {
            'plot_html' : plot_html, 
            'plot_html2': plot_html2,
            }
        
    if (request.GET['model']=="Etude_sur_la_surface"):
        plot_html=prix_m2(foncier2022)
        plot_html2=surface_nb_pieces(foncier2022)
        plot_html3=prix_m2_en_france(foncier2022)
        context = {
            'plot_html' : plot_html, 
            'plot_html2': plot_html2,
            'plot_html3': plot_html3, 
            }
          
    if (request.GET['model']=="Etude_sur_les_types_de_bien"):
        plot_html=types_biens(foncier2019, 2019)
        plot_html3=types_biens(foncier2022, 2022)
        context = {
            'plot_html' : plot_html, 
            'plot_html3': plot_html3, 
            }
        
    if (request.GET['model']=="Cartes"):
        plot_html=map_valeur_fonciere(foncier2022)
        plot_html2=map_ventes_departement(foncier2022)
        plot_html3=map_ventes_idf(foncier2022) # A voir plus tard, ne s'affiche pas pour une raison
        context = {
            'plot_html' : plot_html, 
            'plot_html2': plot_html2,
            #'plot_html3': plot_html3, 
            }

    
    return HttpResponse(template1.render(context, request))