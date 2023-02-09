# Description

A partir de notre jeu de données sur les [météorites](https://www.kaggle.com/nasa/meteorite-landings), trouvé sur le site Kaggle.com et d'autres jeux de données que nous avons combinés avec :
[villes](https://www.kaggle.com/max-mind/world-cities-database?select=worldcitiespop.csv) ainsi que les [continents](https://www.kaggle.com/statchaitya/country-to-continent), 
Hugo Henriques et moi-même (Gabriel Leroux) avons pu élaborer une démarche scientifique afin de comprendre et d'interpréter correctement ces données à travers un dashboard.

## Problématique

En quoi l'humanité à travers la recherche et la découverte de météorites tombées, prend-elle conscience de sa place dans l'univers ? 

## Installation

Au préalable vous devez installer Python et Git sur sa machine :

-	Pour Python, effectuer le téléchargement de la dernière version sur [ce lien](https://www.python.org/downloads/windows/) puis suivez le tutoriel sur cet autre [lien](https://perso.esiee.fr/~courivad/Python/projets/depot.html) afin de finaliser l'installation 
-  	Pour Git, vous devez télécharger la version correspondante (32 ou 64 bits) sur [cette page web](https://git-scm.com/download/win)

### Instruction pour cloner le projet

	$ git clone git@git.esiee.fr:lerouxg/Python.git

### Déplacement dans le répertoire du projet

	$ cd chemin_d'accès/Python.git

### Installation des packages additionnels

La liste des packages additionnels sont dans le fichier **requirements.txt**.

Pour installer ces packages tapez :

	$ python -m pip install -r requirements.txt

Si nécessaire, vous devez faire une mise à jour du pip : 

	$ python.exe -m pip install --upgrade pip

## Démarrage

Instruction à exécuter dans le terminal pour lancer le projet :

    $ python main.py

Cette application est lancée dans une console :

    $ python main.py 
    Dash is running on http://127.0.0.1:8050/

    * Serving Flask app 'main' (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on

Le dashboard peut alors s’observer dans la fenêtre d’un quelconque navigateur à l’adresse indiquée dans la console (ici http://127.0.0.1:8050/)

## Utilisation

> **Vous pouvez adapter le zoom sur les différentes figures présentes dans le dashboard.** 

> **Vous pouvez cliquer sur la légende pour faire apparaître/disparaître certaines données.**

> **Au niveau de la map, vous pouvez cliquer sur les trois boutons, afin de visualiser ce que vous voulez.**

> **Nous avons décider de ne pas supprimer les données des villes, des pays et des continents inconnus (apparues suite au différents merge de jeux de données que nous avons effectués) car nous possédions quand même les coordonnées géographiques. 
Cela implique que dans les graphiques, il y a une catégorie "Unknown" dans laquelle l'entierté des valeurs NaN sont répertoriées.**

## Amélioration possible 

Comme possible amélioration future, il faudrait que chacune des coordonnées géographiques soient associées à une ville, un pays et un continent afin de ne plus avoir de valeurs inconnues.
Cela semble faisable par comparaison des coordonnées géographies des villes et des coordonnées du lieu d'impact de la météorite.

## Conclusion 

Comme réponse à notre problématique, nous avons réussi à établir des liens entre les dates de découverte des météorites ainsi que l'augmentation de ces découvertes en fonction des années.
Nous avons pu constater qu'à partir de 1850, les découvertes des météorites n'étaient plus ponctuelles. En effet, on observe des périodes de 10 à 20 ans de découvertes incessantes de météorites par région suivies de périodes creuses.
Ce phénomène est observable pour toutes les régions du monde. On observe même, qu'il y a une augmentation du nombre de découverte au fur et à mesure du temps. L'homme apporte de plus en plus d'intérêt à ce qui l'entoure, et à sa position dans l'univers. 

Cependant nous n'avons pas réussi à placer en lumière ces points ces arguments dans notre dashboard (difficulté à mettre en place des callbacks des checkbox).
C'est pour cela que dans notre dahsboard, nous avons décidé de ne pas développer ce raisonnement et de rester sur un raisonnement linéaire d'analyse scientifique. 

## Copyright

Nous déclarons sur l'honneur que le code fourni a été produit par nous-même.