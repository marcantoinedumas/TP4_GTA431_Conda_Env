# On commence ici par importer les extentions dont nous allons avoir besoin au cours de notre analyse.
import pandas
import matplotlib.pyplot as plt
from scipy import stats
# Voici la source de nos donnees http://donnees.ville.montreal.qc.ca/dataset/actes-criminels
# Nous avons du separer les donnees en deux fichiers csv, car le fichier etait trop lourd, donc pycharm ne voulait pas le traiter.

# Définition des fonctions
## La fonction imprimer_histogramme nous serviras à afficher l'histogramme selon les différents paramètres qui seront utiles.
def imprimer_histogramme(data_frame, titre, axe_des_X=None, axe_des_Y=None, ajustement_bas=None, ajustement_haut=None, ajustement_gauche=None, ajustement_droite=None):
    data_frame.plot(kind="bar", title=titre)
    plt.xlabel(axe_des_X)  # On nomme l'axe des X
    plt.ylabel(axe_des_Y)  # On nomme l'axe des Y
    plt.subplots_adjust(bottom=ajustement_bas, top=ajustement_haut, left=ajustement_gauche, right=ajustement_droite)  # On ajuste les dimensions du graphique afin de bien afficher les titres
    return plt.show()  # On fait afficher l'histogramme

## La fonction imprimer statistiques qui fait seulement un describe sur un dataframe. Ceci est plus pour l'esthétique qu'autre choses.
def imprimer_statistiques(data_frame):
    print(data_frame.describe())

# Avec pandas, on lis les donnees du csv de 2019 et 2020.
donnees_criminalite_2019 = pandas.read_csv("donnees_criminalite_csv_2019.csv", delimiter=";", parse_dates=["DATE"])
donnees_criminalite_2020 = pandas.read_csv("donnees_criminalite_csv_2020.csv", delimiter=";", parse_dates=["DATE"])

# Ensuite, on met les données dans un dataframe afin de pouvoir les utiliser dans nos analyses
donnees_criminalite_2019_data_frame = pandas.DataFrame(data=donnees_criminalite_2019)  # 2019
donnees_criminalite_2020_data_frame = pandas.DataFrame(data=donnees_criminalite_2020)  # 2020

# On utilise la fonction drop afin d'enlever les colones inutiles dans notre data frame
donnees_criminalite_2019_data_frame = pandas.DataFrame.drop(donnees_criminalite_2019_data_frame, columns= ["PDQ", "X", "Y", "LONGITUDE", "LATITUDE"])  # 2019
donnees_criminalite_2020_data_frame = pandas.DataFrame.drop(donnees_criminalite_2020_data_frame, columns= ["PDQ", "X", "Y", "LONGITUDE", "LATITUDE"])  # 2020

# Étant donné que notre analyses sera sur une base mensuelle, nous allons convertir le format date actuel en mois uniquement.
# NOTE : Il en va de soi que 1 = Janvier, 2 = Février, 3= Mars, 4= Avril, etc.
pandas.DataFrame(donnees_criminalite_2019_data_frame)['DATE'] = pandas.DataFrame(donnees_criminalite_2019_data_frame)['DATE'].dt.month  # 2019
pandas.DataFrame(donnees_criminalite_2020_data_frame)['DATE'] = pandas.DataFrame(donnees_criminalite_2020_data_frame)['DATE'].dt.month  # 2020

# On groupe les données ensemble en utilisant le "groupby" et la fonction aggregate pour calculer le nombre de crimes par mois pour 2019.
crimes_mensuel_2019_data_frame = pandas.DataFrame(donnees_criminalite_2019_data_frame).groupby(['DATE']).agg(
    Nb_Infraction_par_mois_2019=('CATEGORIE', "count"))  # 2019

# Afficher seulement les 4 premiers mois de 2019 pour comparer avec les 4 premiers mois de 2020.
crimes_mensuel_2019_data_frame = pandas.DataFrame(crimes_mensuel_2019_data_frame).drop(crimes_mensuel_2019_data_frame.index[4:12])

# On groupe les données ensemble en utilisant le "groupby" et la fonction aggregate pour calculer le nombre de crimes par mois pour 2020.
crimes_mensuel_2020_data_frame = pandas.DataFrame(donnees_criminalite_2020_data_frame).groupby(['DATE']).agg(
    Nb_Infraction_par_mois_2020=('CATEGORIE', "count"))  # 2020

# Avec la fonction "merge", on regroupe le dataframe de 2019 avec celui de 2020 afin de mieux analyser les données.
crimes_mensuels_2019_2020_data_frame_merged = pandas.merge(left=crimes_mensuel_2019_data_frame, right=crimes_mensuel_2020_data_frame, on='DATE')

# Avec le package matplotlib.pyplot, nous allons représenter graphiquement les données afin de mieux les comparer.
## ANNÉE 2019-2020 (Janvier à Avril) - Nous utilisons les données que nous avons regroupé plus tôt. Nous appelons la fonction définie au début du code afin d'afficher un histogramme.
imprimer_histogramme(data_frame=crimes_mensuels_2019_2020_data_frame_merged, titre="Répartition des actes criminels mensuels sur le territoire \n de Montréal de Janvier à Avril 2019 et 2020",
                     axe_des_X="Mois", axe_des_Y="Nombre d'actes criminels")

# Nous imprimons les statistiques générales que nous allons pouvoir analyser.
imprimer_statistiques(crimes_mensuels_2019_2020_data_frame_merged) # Appel la fonction définie plus haut

# Nous imprimons le tableau de données agrégé
print(crimes_mensuels_2019_2020_data_frame_merged)

# On crée une liste avec les données mensuelles du premier quadrimestre de chaque année
liste_crimes_mensuel_2019 = crimes_mensuel_2019_data_frame['Nb_Infraction_par_mois_2019'].to_list()
liste_crimes_mensuel_2020 = crimes_mensuel_2020_data_frame['Nb_Infraction_par_mois_2020'].to_list()

# On calcule et on affiche la variation de janvier à avril pour 2019
variation_janvier_a_avril_2019 = round((liste_crimes_mensuel_2019[3] - liste_crimes_mensuel_2019[0]) / liste_crimes_mensuel_2019[0], 4)
print(variation_janvier_a_avril_2019)

# On calcule et on affiche la variation de janvier à avril pour 2020
variation_janvier_a_avril_2020 = round((liste_crimes_mensuel_2020[3] - liste_crimes_mensuel_2020[0]) / liste_crimes_mensuel_2020[0], 4)
print(variation_janvier_a_avril_2020)

# On calcule et on affiche la variation de mars à avril pour 2020
variation_mars_avril_2020 = round((liste_crimes_mensuel_2020[3] - liste_crimes_mensuel_2020[2]) / liste_crimes_mensuel_2020[2], 4)
print(variation_mars_avril_2020)

# On calcul et on imprime le khi2 et la valeur p ; hypothèse - les crimes de 2019 se répartissent normalement d'année en année
print(stats.chisquare(liste_crimes_mensuel_2020, liste_crimes_mensuel_2019))
