# On commence ici par importer les extentions dont nous allons avoir besoin au cours de notre analyse.
import pandas
import matplotlib.pyplot as plt

# Avec pandas, on lis les donnees du csv de 2019 et 2020.
# Voici la source de nos donnees http://donnees.ville.montreal.qc.ca/dataset/actes-criminels
# Nous avons du separer les donnees en deux fichiers csv, car le fichier etait trop lourd, donc pycharm ne voulait pas le traiter.
donnees_criminalite_2019 = pandas.read_csv("donnees_criminalite_csv_2019.csv", delimiter=";", parse_dates=["DATE"])
donnees_criminalite_2020 = pandas.read_csv("donnees_criminalite_csv_2020.csv", delimiter=";", parse_dates=["DATE"])

# Avec le groupby ici on compte le nombre d'actes criminels en les groupant par mois.
compilation_crimes_mensuel_2019 = donnees_criminalite_2019.groupby(donnees_criminalite_2019["DATE"].dt.month).count()["CATEGORIE"]
compilation_crimes_mensuel_2020 = donnees_criminalite_2020.groupby(donnees_criminalite_2020["DATE"].dt.month).count()["CATEGORIE"]
print(compilation_crimes_mensuel_2020)

# On veut afficher un diagramme de type "histogramme" afin de visualiser le nombre total d'actes crimimels repertories par mois sur le territoire de Montreal.
# Pour l'annee 2019 (Janvier a Decembre)
compilation_crimes_mensuel_2019.plot(kind="bar", title="Répartition des actes criminels par mois \n sur le territoire de Montréal pour 2019")
plt.ylabel("Nombre d'actes criminels") # Donner un titre a l'axe des y
plt.xlabel("Mois") # Donner un titre a l'axe des x
plt.show() # Afficher le graphique
# Pour l'annee 2020 (Janvier au 24 Avril)
compilation_crimes_mensuel_2020.plot(kind="bar", title="Répartition des actes criminels par mois sur le \n territoire de Montréal de Janvier 2020 au 24 Avril 2020")
plt.ylabel("Nombre d'actes criminels") # Donner un titre a l'axe des y
plt.xlabel("Mois") # Donner un titre a l'axe des x
plt.show() # Afficher le graphique

# Infraction jour/nuit par mois


# Grouper par type d'infration - on veut savoir le nombre et la proportion de tous les crimes (Proportion infraction_specifique/total_infraction)