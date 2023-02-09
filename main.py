"""
Ce programme permet de :
traiter des fichiers .csv,
créer des figures basées sur ces données
et créer un dashboard permettant une meilleure lisibilité des données.
Il a été réalisé dans le cadre de la réalisation du mini projet Open Data.

Auteurs : Henriques Hugo & Leroux Gabriel
Date : 02/01/2022
"""
### Imports ###
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

###========================== TRAITEMENT DES DONNEES ===================================###

# On transforme les datasets originales téléchargés sur kaggle.com en des dataframes
# Notre dataframe de base :
meteorites=pd.read_csv('meteorite-landings.csv')
# lien : https://www.kaggle.com/nasa/meteorite-landings
# Pour ajouter les pays à notre dataframe :
cities=pd.read_csv('worldcitiespop.csv')
# lien : https://www.kaggle.com/max-mind/world-cities-database?select=worldcitiespop.csv
# Pour ajouter les continents :
continents=pd.read_csv('countryContinent.csv',encoding='utf8')
# lien : https://www.kaggle.com/statchaitya/country-to-continent

# 1. Traitons les météorites
# On supprime les colonnes qui ne nous serviront pas
meteorites = meteorites.drop(['id'],1)
meteorites = meteorites.drop(['nametype'],1)
# On supprime les valeurs d'années aberrantes
meteorites = meteorites[meteorites['year']<2021]
# Ainsi que les années précédent 1800 car trop peu de données avant cette date
meteorites = meteorites[meteorites['year']>1800]
# On supprime les météorites observées non retrouvées
meteorites = meteorites[meteorites['fall']=='Found']
meteorites = meteorites.drop(['fall'],1)

# 2. Traitons les villes
# On supprime les colonnes qui ne nous serviront pas
cities = cities.drop(['Population'],1)
cities = cities.drop(['Region'],1)
cities = cities.drop(['City'],1) # Parce qu'on ne s'interesse seulement à AccentCity
# Ici ce qui nous interresse ce sont les coordonnées des meteorites, pas celles des villes
cities = cities.drop(['Latitude'],1)
cities = cities.drop(['Longitude'],1)

# 3. Traitons les continents
# On supprime les colonnes qui ne nous serviront pas
# Ici ce que l'on veux récupérer ce sont les continents
continents = continents.drop(['code_3'],1)
continents = continents.drop(['country_code'],1)
continents = continents.drop(['iso_3166_2'],1)
continents = continents.drop(['sub_region'],1)
continents = continents.drop(['region_code'],1)
continents = continents.drop(['sub_region_code'],1)

###################################
##### 4. Merge des dataframes #####
###################################

# On renomme la colonne name afin de merger
rename = {'name': 'AccentCity'}
meteorites.rename(columns=rename, inplace=True)

# On élimine les valeurs dupliquées qui ne sont pas bonnes pour un merge
cities = cities.drop_duplicates(subset='AccentCity')

# On peut enfin merger notre df de météorites et celle des villes en fonction de City
newDf=pd.merge(meteorites,cities, on=['AccentCity'],how='left')

# On supprime les lignes ne possédant pas de Geolocalisation
newDf = newDf[newDf['GeoLocation'].notna()]

# On renomme la colonne name pour un soucis de compréhension après avoir mergé les bonnes colonnes
# ainsi que la colonne Country en country code afin d'avoir par la suite le country et le continent
rename = {'AccentCity': 'City'}
newDf.rename(columns={'AccentCity': 'City', 'Country': 'code_2'}, inplace=True)

# On met toute la colonne code de newDf en majuscule comme dans continents afin de merger
newDf['code_2'] = newDf['code_2'].astype(str).str.upper()

# On peut enfin merger notre df principal avec celle des continents en fonction de code_2
maindf=pd.merge(newDf,continents, on=['code_2'],how='left')

# On remplace les Nans qui sont apparus
maindf['code_2'].fillna('XX', inplace=True)
maindf['country'].fillna('Unknown', inplace=True)
maindf['continent'].fillna('Unknown', inplace=True)

####################################################
##### 5. Création de données dataframes utiles #####
####################################################

# On créé les différentes sous-dataframe avec la classification des types de météorite :
# source : https://en.wikipedia.org/wiki/Meteorite_classification
# On créé un ensemble de données pour chaque type de météorite

# stony materials
ToutesLesL =    maindf[maindf['recclass'].str.contains('^L.*')]
ToutesLesH =    maindf[maindf['recclass'].str.contains('^H.*')]
ToutesLesE =    maindf[maindf['recclass'].str.contains('^E.*')]
ToutesLesC =    maindf[maindf['recclass'].str.contains('^C.*')]
Ureilite =      maindf[maindf['recclass'].str.contains('Ureilite')]
Diogenite =     maindf[maindf['recclass'].str.contains('^Diogenite.*')]
Eucrite =       maindf[maindf['recclass'].str.contains('^Eucrite.*')]
Angrite =       maindf[maindf['recclass'].str.contains('^Angrite.*')]
Aubrite =       maindf[maindf['recclass'].str.contains('^Aubrite.*')]
Howardite =     maindf[maindf['recclass'].str.contains('^Howardite.*')]
Stone =         maindf[maindf['recclass'].str.contains('^Stone.*')]
Martian =       maindf[maindf['recclass'].str.contains('^Martian.*')]

stony = pd.concat(
    [ToutesLesL,ToutesLesH, ToutesLesE, ToutesLesC,
    Ureilite, Diogenite, Angrite, Aubrite, Howardite, Stone, Martian]
)

# iron materials
iron = maindf[maindf['recclass'].str.contains('^Iron.*')]

# stony-iron materials
Mesosiderite = maindf[maindf['recclass'].str.contains('^Mesosiderite.*')]
Pallasite = maindf[maindf['recclass'].str.contains('^Pallasite.*')]

stony_iron = pd.concat([Pallasite,Mesosiderite])

# Moyenne de la masse totale pour chaque année
mass_moy = maindf[['year','mass']].groupby('year').mean()

# Création d'une sous dataframe sans les énormes météorites (>1T)
withoutBiggest = maindf[maindf['mass']<1000000]

###========================== TRAITEMENT DES DONNEES ===================================###

###=========================== CREATION DU CONTENUE ====================================###

################################################
##### 1. Création des figures du dashboard #####
################################################

# On créé une courbe, px.line permet d'avoir des courbes, ici on veut
# la masse moyenne des météorites retrouvées en fonction de l'année de 1800 à 2013
massMoy = px.line(mass_moy,x= mass_moy.index, y= "mass")

# On créé un histogramm afin d'observer en détails les années où
# il y a des augmentation de masse de météorites retrouvés
barChart = px.bar(maindf, x="year", y="mass", color='continent')

# On créé le même histogramm mais cette fois ci sans les grosses météorites
barChartMin = px.bar(withoutBiggest, x="year", y="mass", color='continent')

# On créé 3 diagramme qui permettront de montrer la composition des météorites
# en fonction des trois catégories : rocheuse, ferreuse et mixte
stonyPie = px.pie(stony, names='recclass')
stonyPie.update_traces(textinfo='percent+label',textposition='inside')

ironPie = px.pie(iron, names='recclass')
ironPie.update_traces(textinfo='percent+label',textposition='inside')

stonyIronPie = px.pie(stony_iron, names='recclass')
stonyIronPie.update_traces(textinfo='percent+label',textposition='inside')

# On créé 3 Map qui permettront de placer les météorites
# selon 3 catégories : rocheuse , ferreuse et mixte
stonyGeo = go.Figure(
    data=go.Scattergeo(
        lat = stony['reclat'],
        lon = stony['reclong'],
        text =
        "Ville : "+ stony['City'] + "[" + stony['code_2'] +
        "]." + '\n' + " Année de crash : " + stony['year'].astype(str) +
        '\n' + "Masse : " + stony['mass'].astype(str) + "g.",
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = True,
            symbol =  'octagon',
            line = dict(
                width=1,
                color='brown'
            ),
        )
    )
)
ironGeo = go.Figure(
    data=go.Scattergeo(
        lat = iron['reclat'],
        lon = iron['reclong'],
        text =
        "Ville : "+ iron['City'] + "[" + iron['code_2'] +
        "]." + '\n' + " Année de crash : " + iron['year'].astype(str) +
        '\n' + "Masse : " + iron['mass'].astype(str) + "g.",
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = True,
            symbol = 'triangle-down',
            line = dict(
                width=1,
                color='goldenrod'
            ),
        )
    )
)
stonyIronGeo = go.Figure(
    data=go.Scattergeo(
        lat = stony_iron['reclat'],
        lon = stony_iron['reclong'],
        text =
        "Ville : "+ stony_iron['City'] + "[" + stony_iron['code_2'] +
        "]." +'\n' + " Année de crash : " + stony_iron['year'].astype(str) +
        '\n' + "Masse : " + stony_iron['mass'].astype(str) + "g.",
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = True,
            symbol = 'star-diamond-dot',
            line = dict(
                width=1,
                color='violet'
            ),
        )
    )
)

######################################################
##### 2. Création de aspects visuels des figures #####
######################################################

# On créé notre palette de couleur qu'on utilisera pour l'esthétique de notre dashboard
colors = {
    'background': '#111111',
    'text': '#27BBE8',
    'legend': '#BD99D2',
    'title': '#864BFD'
}

# Réglages graphiques qu'on reproduit avec toutes les figures
massMoy.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title']
    )
barChart.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title']
    )
barChartMin.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title'
    ])
stonyPie.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title']
    )
ironPie.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title']
    )
stonyIronPie.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title']
    )
stonyGeo.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title']
    )
ironGeo.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title']
    )
stonyIronGeo.update_layout(
    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['title']
    )

###=========================== CREATION DU CONTENUE ====================================###

###======================== MISE EN PLACE DU DASHBOARD =================================###

# On créé une instance de la classe dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# On créé le titre du dashboard
app.title = 'Dashbord Météorites'

# La mise en page en dash se déroule grâce app.layout c'est à l'interieur du layout
# que l'on va insérer le texte et l'odre d'appartion des graphiques
# Pour pouvoir afficher les figures de notre dashboard l'ordre compte !
app.layout = html.Div([
    ### Titre ###
    html.Br(),
    html.H1(children=
        'Dashboard sur les météorites pénétrant l\'atmosphère terrestre',
        style={'textAlign': 'center', 'color': colors['title']}
        ),
    ### Intro + Courbe ###
    html.Div(
        children=[
            html.Br(),
            html.Div(
                '''Les météorites ont toujours existées et aujourd'hui encore
                il en tombe tous les jours sur Terre. On va chercher a développer
                un raisonnement scientifique en observant les différents affichages
                de données que nous allons effectuer. L'entièreté des météorites dont
                nous allons parler ont été retrouvées tout autour de notre planète.''',
                style={'textAlign': 'justify', 'color': colors['text']}
            ),
            html.Br(),
            html.Div(
                '''Pour commencer, voici la définition d'une météorite d'après Futura
                Sciences :"Corps rocheux d'origine extraterrestre qui a survécu à la
                traversée de l'atmosphère et qu'on retrouve donc sur le sol terrestre."''',
                style={'textAlign': 'justify', 'color': colors['text']}
            ),
            html.Br(),
            html.H2(children=
                '''Masse moyenne(en g) des météorites retrouvées de l'année 1800 à 2013''',
                style={'textAlign': 'center', 'color': colors['title']}
            ),
            dcc.Graph(
                id='graph0',
                figure=massMoy,
                style={'textAlign': 'center','width' : '750'}
            ),
            html.Div(
                '''On observe que la moyenne de la masse de météorites retrouvées
                par an subit de nombreuses variations mais elles ne dur qu'un an.
                Nous allons donc créer un histogramme afin d'en savoir plus sur
                les météorites découvertes lors de ces années.''',
                style={'textAlign': 'justify', 'color': colors['text']}
            ),
        ],
        style={'color':colors['background'], 'display':'inline-block', 'width': '2100'}
    ),
    ### Histogrammes ###
    html.Div(
        children=[
            html.Br(),
            html.H2(children=
                '''Histogramme représentant les masses totales des météorites
                retrouvées de l'année 1800 à 2013 dans le monde (en gramme)''',
                style={'textAlign': 'center', 'color': colors['title']}
            ),
            dcc.Graph(
                id='graph1',
                figure=barChart,
                style={'textAlign': 'center'}
            ),
            html.Div(
                ''' On comprend d'après cette histogramme et d'après ses variations
                irrégulières et conséquentes que d'énormes météorites ont été trouvées
                certaines années. Elles brisent donc l'uniformité de la moyenne globale,
                que nous n'afficherons donc pas. Affichons maintenant le même histogramme
                mais en excluant les météorites de plus d'une tonne.''',
                style={'textAlign': 'justify', 'color':colors['text']}
            ),
            html.Br(),
            html.H2(children=
                '''Histogramme représentant les masses totales des météorites retrouvées
                inférieures à 1 Tonne de l'année 1800 à 2013 dans le monde (en gramme)''',
                style={'textAlign': 'center', 'color': colors['title']}
            ),
            dcc.Graph(
                id='graph2',
                figure=barChartMin,
                style={'textAlign': 'center'}
            ),
            html.Div(
                '''Cet histogramme nous permet de comprendre que le poids des météorites
                varie énormément. Nous allons donc nous intéresser a chacun des types de
                météorites ainsi qu'à leur composition.''',
                style={'textAlign': 'justify', 'color':colors['text']}
            ),
            html.Br()
        ],
        style={'color':colors['background'], 'display':'inline-block', 'width': '2100'}
    ),
    ### Pie ###
    html.Div(
        children=[
            html.Br(),
            html.Div(
                '''D'après la classification scientifique de Wikipedia
                (https://en.wikipedia.org/wiki/Meteorite_classification), il existe trois
                types de météorites : les météorites ferreuses, les météorites rocheuses,
                et les météorites mixtes. On les classe selon les éléments qui les constitut.
                La suite est simple, si ces éléments sont d'origine rocheuses, la météorites
                sera classée rocheuses. Si ces éléments sont ferreux, la météorites sera
                ferreuse et si la météorite est composée d'éléments hybrides (ferreux et
                rocheux), elle sera classée comme mixte. Parmi ces trois types, il existe un
                tas de cas différents selon les éléments qui constituent la météorite.''',
                style={'textAlign': 'justify', 'color':colors['text']}
            ),
            html.Br(),
            html.H2(children=
            '''Diagrammes circulaires de la moyenne des compositions de
            chaque type de météorites''',
            style={'textAlign': 'center', 'color': colors['title']}
            ),
            html.Div(
                children=[
                    html.H3(children=
                        '''-----------------Rocheuse------------------|''',
                        style={'textAlign': 'center', 'color': colors['title']}
                    ),
                    dcc.Graph(
                        id='graph4',
                        figure=stonyPie
                    )
                ],
                className="pie1",
                style={
                    'display':'inline-block',
                    'position' : 'relative',
                    'height' : '800', 'width' : '700'
                }
            ),
            html.Div(
                children=[
                    html.H3(children=
                        '''----------------Ferreuse-----------------''',
                        style={'textAlign': 'center', 'color': colors['title']}
                    ),
                    dcc.Graph(
                        id='graph5',
                        figure=ironPie,
                        style={'textAlign': 'center'}
                    )
                ],
                className="pie2",
                style={
                    'display':'inline-block',
                    'position' : 'relative',
                    'height' : '800', 'width' : '700'
                }
            ),
            html.Div(
                children=[
                    html.H3(children=
                        '''|-----------------Mixte-------------------''',
                        style={'textAlign': 'center', 'color': colors['title']}
                    ),
                    dcc.Graph(
                        id='graph6',
                        figure=stonyIronPie
                    ),
                ],className="pie3",
                style={
                    'display':'inline-block',
                    'position' : 'relative',
                    'height' : '800', 'width' : '700'
                }
            ),
        ],
        style={
                'position' : 'relative',
                'display':'inline',
                'height' : 'auto',
                'width' : 'auto',
                'background-color' : colors['background']
        }
    ),
    ### Map
    html.Div(
        children=[
            html.H2(children=
                '''Carte des lieux d'impacte de météorites de type ...''',
                id="title-geo",
                style={'textAlign': 'center', 'color': colors['title']}
            ),
            html.Div(
                '''Choisissez le type de météorite que vous voulez afficher
                sur la carte ci-dessous.''',
                style={'textAlign': 'justify', 'color':colors['text']}
            ),
            html.Br(),
            html.Label(
                'Météorites de type : ',
                style={'color': colors['title']}
            ),
            dcc.RadioItems(
                id='meteorites-type-radio',
                options=[
                    {'label': 'Rocheuse', 'value': 'stony'},
                    {'label': 'Ferreuse', 'value': 'iron'},
                    {'label': 'Mixte', 'value': 'stony-iron'}
                ],
                style={'color':colors['text']},
                value='stony-iron'
            ),
            dcc.Graph(
                id='graph7',
                figure=stonyIronGeo
            )
        ],
    ),
    html.Div(
        children=[
            html.Br(),
            html.Div(children=
                '''Copyrights : Ce dashbord a été entièrement réalisé par
                Henriques Hugo & Leroux Gabriel''',
                style={'textAlign': 'center', 'color': colors['legend']}
            ),
            html.Div(children=
                '''Sources : Wikipédia, Futura Sciences''',
                style={'textAlign': 'center', 'color': colors['legend']}
            ),
            html.Div(children=
                '''Jeu de données utilisés (Kaggle.com) :
                meteorite-landings.csv, worldcitiespop.csv, countryContinent.csv''',
                style={'textAlign': 'center', 'color': colors['legend']}
            )
        ],
    )
], style={'backgroundColor': colors['background'], 'margin' : '0', 'width': '2300'})

### callbacks

@app.callback(
    Output(component_id='graph7', component_property='figure'),
    Input(component_id='meteorites-type-radio', component_property='value')
)
def update_scattergeo(input_value):
    """
    Retourne la figure géographique en fonction de la valeur du RadioItems

    Args:
        input_value

    Returns:
        update_scattergeo(input_value) : go.Figure( data=go.Scattergeo(...) )
    """
    if input_value == "stony"       :
        return stonyGeo
    if input_value == "iron"        :
        return ironGeo
    #if input_value == "stony-iron"  :
    return stonyIronGeo

@app.callback(
    Output(component_id='title-geo', component_property='children'),
    Input(component_id='meteorites-type-radio', component_property='value')
)
def update_title_geo(input_value):
    """
    Retourne le nom de la figure géographique en fonction de la valeur du RadioItems

    Args:
        input_value

    Returns:
        update_title_geo(input_value) : 'title...'
    """
    if input_value == "stony"       :
        return '''Carte des lieux d'impacte de météorites de type rocheuse'''
    if input_value == "iron"        :
        return '''Carte des lieux d'impacte de météorites de type ferreuse'''
    #if input_value == "stony-iron"  :
    return '''Carte des lieux d'impacte de météorites de type mixte'''

###======================== MISE EN PLACE DU DASHBOARD =================================###

if __name__ == '__main__':
    app.run_server(debug=True)