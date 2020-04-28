# On commence ici par importer les extentions dont nous allons avoir besoin au cours de notre analyse.
import pandas
import matplotlib.pyplot as plt

# Voici la source de nos donnees http://donnees.ville.montreal.qc.ca/dataset/actes-criminels
# Nous avons du separer les donnees en deux fichiers csv, car le fichier etait trop lourd, donc pycharm ne voulait pas le traiter.

# On définie des fonctions qui seront utiles tout au long de l'analyse
## Premièrement la fonction imprimer_histogramme nous serviras à afficher l'histogramme selon les différents paramètres qui seront utiles.
### Nous avons décidé de définir la fonction afin de rendre le code plus beau et moins chargé, vu le fait que nous allons afficher 3 fois des histogrammes.
def imprimer_histogramme(data_frame, titre, axe_des_X=None, axe_des_Y=None, ajustement_bas=None, ajustement_haut=None, ajustement_gauche=None, ajustement_droite=None):
    data_frame.plot(kind="bar", title=titre)
    plt.xlabel(axe_des_X)  # On nomme l'axe des X
    plt.ylabel(axe_des_Y)  # On nomme l'axe des Y
    plt.subplots_adjust(bottom=ajustement_bas, top=ajustement_haut, left=ajustement_gauche, right=ajustement_droite)  # On ajuste les dimensions du graphique afin de bien afficher les titres
    return plt.show()  # On fait afficher l'histogramme

## Deuxièmement, nous avons créé la fonction imprimer statistiques qui fait seulement un describe sur un dataframe. Ceci est plus pour l'esthétique qu'autre choses.
def imprimer_statistiques(data_frame):
    print(data_frame.describe())


# Avec pandas, on lis les donnees du csv de 2019 et 2020.
donnees_criminalite_2019 = pandas.read_csv("donnees_criminalite_csv_2019.csv", delimiter=";", parse_dates=["DATE"])
donnees_criminalite_2020 = pandas.read_csv("donnees_criminalite_csv_2020.csv", delimiter=";", parse_dates=["DATE"])

# Ensuite, on met les données dans un dataframe afin de pouvoir les utiliser dans nos analyses
## Pour 2019
donnees_criminalite_2019_data_frame = pandas.DataFrame(data=donnees_criminalite_2019)
## Pour 2020
donnees_criminalite_2020_data_frame = pandas.DataFrame(data=donnees_criminalite_2020)

# On utilise la fonction drop afin d'enlever les colones inutiles dans notre data frame
## Pour 2019
donnees_criminalite_2019_data_frame = pandas.DataFrame.drop(donnees_criminalite_2019_data_frame, columns= ["PDQ", "X", "Y", "LONGITUDE", "LATITUDE"])
## Pour 2020
donnees_criminalite_2020_data_frame = pandas.DataFrame.drop(donnees_criminalite_2020_data_frame, columns= ["PDQ", "X", "Y", "LONGITUDE", "LATITUDE"])

# Étant donné que nos analyses seront toujours sur une base mensuelle, nous allons tout de suite convertir le format date actuel en mois uniquement.
# NOTE : Il en va de soi que 1 = Janvier, 2 = Février, 3= Mars, 4= Avril, etc.
## Pour 2019
pandas.DataFrame(donnees_criminalite_2019_data_frame)['DATE'] = pandas.DataFrame(donnees_criminalite_2019_data_frame)['DATE'].dt.month
## Pour 2020
pandas.DataFrame(donnees_criminalite_2020_data_frame)['DATE'] = pandas.DataFrame(donnees_criminalite_2020_data_frame)['DATE'].dt.month


############ PREMIÈRE ANALYSE - NOMBRE TOTAL D'ACTES CRIMINELS PAR MOIS ############
# Avec cette analyse, on tente de se faire un première vision générale de la situation avant de pousser nos analyses.
# On tente de démontrer que le confinement à un lien avec la diminution du nombre de crimes sur l'ile de Montréal en comparant avec les données à pareille date l'an dernier.

# ÉTAPE 1: Avec le groupby ici on compte le nombre d'actes criminels en les groupant par mois.
## POUR L'ANNÉE 2019
### On groupe les données ensemble en utilisant le "groupby" et la fonction aggregate pour calculer le nombre de crimes par mois.
crimes_mensuel_2019_data_frame = pandas.DataFrame(donnees_criminalite_2019_data_frame).groupby(['DATE']).agg(
    Nb_Infraction_par_mois_2019=('CATEGORIE', "count"))
### Afficher seulement les 4 premiers mois de 2019 pour comparer avec les 4 premiers mois de 2020.
crimes_mensuel_2019_data_frame = pandas.DataFrame(crimes_mensuel_2019_data_frame).drop(crimes_mensuel_2019_data_frame.index[4:12])

## POUR L'ANNÉE 2020
### On groupe les données ensemble en utilisant le "groupby" et la fonction aggregate pour calculer le nombre de crimes par mois.
crimes_mensuel_2020_data_frame = pandas.DataFrame(donnees_criminalite_2020_data_frame).groupby(['DATE']).agg(
    Nb_Infraction_par_mois_2020=('CATEGORIE', "count"))

# ÉTAPE 2: Avec la fonction "merge", on regroupe le dataframe de 2019 avec celui de 2020 afin de mieux analyser les données.
crimes_mensuels_2019_2020_data_frame_merged = pandas.merge(left=crimes_mensuel_2019_data_frame, right=crimes_mensuel_2020_data_frame, on='DATE')

# ÉTAPE 3: Avec le package matplotlib.pyplot, nous allons représenter graphiquement les données afin de mieux les comparer.
## ANNÉE 2019-2020 (Janvier à Avril) - Nous utilisons les données que nous avons regroupé à l'étape 2. Nous appelons la fonction définie au début du code afin d'afficher un histogramme.
imprimer_histogramme(data_frame=crimes_mensuels_2019_2020_data_frame_merged, titre="Répartition des actes criminels mensuels sur le territoire \n de Montréal de Janvier à Avril 2019 et 2020",
                     axe_des_X="Mois", axe_des_Y="Nombre d'actes criminels")

# ÉTAPE 4: Nous imprimons les statistiques que nous allons pouvoir analyser.
imprimer_statistiques(crimes_mensuels_2019_2020_data_frame_merged) # Appel la fonction définie plus haut

############ DEUXIÈME ANALYSE - NOMBRE TOTAL D'ACTES CRIMINELS MENSUELS PAR QUART ############
# Avec cette analyse, on tente de voir s'il y a eu un changement au niveau du temps de la journée ou les actes criminels sont produit.
# En d'autres mots, est-ce que le confinement vient modifier l'habitude des criminels en ce qui a trait au temps où ils comettent leur crimes.

# ÉTAPE 1: Avec le groupby ici on compte le nombre d'actes criminels en les groupant par quart et par mois.
## POUR L'ANNÉE 2019
### On groupe les données ensemble en utilisant le "groupby" et la fonction aggregate pour calculer le nombre de crimes par mois et par quart.
crimes_mensuels_par_quart_2019_data_frame = pandas.DataFrame(donnees_criminalite_2019_data_frame).groupby(['DATE', 'QUART']).agg(
    Nb_Infraction_Par_Quart_2019=('CATEGORIE', "count"))
### Afficher seulement les 4 premiers mois de 2019 pour comparer avec les 4 premiers mois de 2020.
crimes_mensuels_par_quart_2019_data_frame = pandas.DataFrame(crimes_mensuels_par_quart_2019_data_frame).drop(crimes_mensuels_par_quart_2019_data_frame.index[12:36])

## POUR L'ANNÉE 2020
### On groupe les données ensemble en utilisant le "groupby" et la fonction aggregate pour calculer le nombre de crimes par mois et par quart.
crimes_mensuels_par_quart_2020_data_frame = pandas.DataFrame(donnees_criminalite_2020_data_frame).groupby(['DATE', 'QUART']).agg(
    Nb_Infraction_Par_Quart_2020=('CATEGORIE', "count"))

# ÉTAPE 2: Avec la fonction "merge", on regroupe le dataframe de 2019 avec celui de 2020 afin de mieux analyser les données.
crimes_mensuels_par_quart_2019_2020_data_frame_merged = pandas.merge(left=crimes_mensuels_par_quart_2019_data_frame, right=crimes_mensuels_par_quart_2020_data_frame, on=['DATE', 'QUART'])

# ÉTAPE 3: Avec le package matplotlib.pyplot, nous allons représenter graphiquement les données afin de mieux les comparer.
## ANNÉE 2019-2020 (Janvier à Avril) - Nous utilisons les données que nous avons regroupé à l'étape 2. Nous appelons la fonction définie au début du code afin d'afficher un histogramme.
imprimer_histogramme(data_frame=crimes_mensuels_par_quart_2019_2020_data_frame_merged, titre="Répartition des actes criminels mensuels par quart de travail \n sur le territoire de Montréal de Janvier à Avril 2019 et 2020",
                     axe_des_X="Mois, Quart", axe_des_Y="Nombre d'actes criminels", ajustement_bas=0.19)

# ÉTAPE 4: Nous imprimons les statistiques que nous allons pouvoir analyser.
imprimer_statistiques(crimes_mensuels_par_quart_2019_2020_data_frame_merged) # Appel la fonction définie au début du code

############ TROISIEME ANALYSE - Crimes par catégorie de crime par mois ############
# Grouper par type d'infration - on veut savoir le nombre et la proportion de tous les crimes (Proportion infraction_specifique/total_infraction)

# ÉTAPE 1: Avec le groupby ici on compte le nombre d'actes criminels en les groupant par catégorie et par mois.
## POUR L'ANNÉE 2019
### On groupe les données ensemble en utilisant le "groupby" et la fonction aggregate pour calculer le nombre de crimes par mois et par catégorie.
crimes_mensuels_par_categorie_2019_data_frame = pandas.DataFrame(donnees_criminalite_2019_data_frame).groupby(['DATE', 'CATEGORIE']).agg(
    Nb_Infraction_Par_Categorie_2019=('CATEGORIE', "count"))
### Afficher seulement les 4 premiers mois de 2019 pour comparer avec les 4 premiers mois de 2020 (drop index).
crimes_mensuels_par_categorie_2019_data_frame = pandas.DataFrame(crimes_mensuels_par_categorie_2019_data_frame).drop(crimes_mensuels_par_categorie_2019_data_frame.index[22:68])

## POUR L'ANNÉE 2020
### On groupe les données ensemble en utilisant le "groupby" et la fonction aggregate pour calculer le nombre de crimes par mois et par catégorie.
crimes_mensuels_par_categorie_2020_data_frame = pandas.DataFrame(donnees_criminalite_2020_data_frame).groupby(['DATE', 'CATEGORIE']).agg(
    Nb_Infraction_Par_Categorie_2020=('CATEGORIE', "count"))

# ÉTAPE 2: Avec la fonction "merge", on regroupe le dataframe de 2019 avec celui de 2020 afin de mieux analyser les données.
crimes_mensuels_par_categorie_2019_2020_data_frame_merged = pandas.merge(left=crimes_mensuels_par_categorie_2019_data_frame, right=crimes_mensuels_par_categorie_2020_data_frame, on=['DATE', 'CATEGORIE'])

# ÉTAPE 3: Avec le package matplotlib.pyplot, nous allons représenter graphiquement les données afin de mieux les comparer.
## ANNÉE 2019-2020 (Janvier à Avril) - Nous utilisons les données que nous avons regroupé à l'étape 2. Nous voulons un diagramme de type "histogramme". Appel la fonction imprimer_histogramme
imprimer_histogramme(data_frame=crimes_mensuels_par_categorie_2019_2020_data_frame_merged, titre="Répartition des actes criminels mensuels par catégorie de crime \n sur le territoire de Montréal de Janvier à Avril 2019 et 2020",
                     axe_des_X="Mois, Categorie", axe_des_Y="Nombre de crimes", ajustement_bas=0.56, ajustement_haut=0.91, ajustement_gauche=0.10, ajustement_droite=0.96)

# ÉTAPE 4: Nous imprimons les statistiques que nous allons pouvoir analyser.
imprimer_statistiques(crimes_mensuels_par_categorie_2019_2020_data_frame_merged) # Appel la fonction définie au début du code