# BabelioTagScrapping
Un script python permettant de constituer sa propre base de donnée de livre et ses étiquettes pour faire des recherches plus précise.

Ce script créer un base de donnée SQLite regroupant les livres que vous voulez ajouter ainsi que divers infos le concernant (Note, nombre de lecteur, nombre de critique....) mais surtout les tags associés au livre.
Cela permet derrière de faire de meilleure recherche à l'aide de requete SQL.

Afin de constituer votre base de donnée je conseille d'utiliser l'extention Link klipper sur Chrome et de le parametrer en rentrant babelio.com/livres/ dans la rubrique regex. Vous n'avez plus qu'a extraire tous les liens présent sur plusieurs page babelio et à mettre les fichier csv les regroupants dans un dossier nommé csv_files.
Vous n'avez plus qu'à run le corps.py .

