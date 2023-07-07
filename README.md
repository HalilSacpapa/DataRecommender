# T-DAT-901-LYO_19

# Recommender

### Bienvenue sur le dépôt du projet Recommender.

## Installation

Pour installer le projet, suivez les étapes suivantes:

##### Pour la data visualisation :
- Téléchargez ou clonez le dépôt sur votre ordinateur
- Ouvrez un terminal et accédez au répertoire du projet
- Exécutez la commande `npm install` pour installer les dépendances

##### Pour le systèlme de recommendation :
- Exécutez la commande `pip install -r requirements.txt` pour installer les dépendances Python
- Sur un terminal dans le répertoire `GUI/`, exécutez la commande `python app.py`

*L'application Flask sera disponible à l'URL `http://localhost:8000/`*

## Utilisation

Pour utiliser le projet, suivez les étapes suivantes:

- Ouvrez un terminal et accédez au répertoire du projet
- Exécutez la commande npm start pour lancer l'application
- Suivez les instructions affichées dans le terminal pour utiliser le projet

## Requirements - Data Exploration

1. Docker installé sur l'ordinateur local
2. Docker Compose installé sur l'ordinateur local
3. Accès à internet pour télécharger les images Docker nécessaires
4. Connaissances de base sur l'utilisation de Docker et Docker Compose
5. Un fichier docker-compose.yml présent dans le répertoire du projet
6. Les ports 5432 et 3000 doivent être disponibles pour les services PostgreSQL et Metabase respectivement
7. Éventuellement, une configuration spécifique pour le réseau Docker (si vous avez d'autres services en cours d'exécution sur le même réseau)

Après avoir vérifié que toutes les exigences sont remplies, vous pouvez exécuter la commande docker-compose up pour démarrer les services PostgreSQL et Metabase.

## Nettoyage des données

Voici comment nettoyer mon dataframe df en utilisant pandas pour m'assurer que les données sont propres et sûres :

1. Vérifier les valeurs manquantes dans chaque colonne en utilisant la méthode df.isnull().sum()
2. Remplir les valeurs manquantes avec une valeur par défaut ou en utilisant la valeur moyenne, la valeur la plus fréquente, etc. en utilisant les méthodes df.fillna() ou df.replace()
3. Vérifier les données aberrantes dans chaque colonne en utilisant des méthodes de visualisation de données telles que df.plot() ou df.boxplot()
4. Supprimer les données aberrantes en utilisant la méthode df.drop()
5. Vérifier la cohérence des données en utilisant des méthodes de vérification de données telles que df.duplicated() ou df.groupby()
6. Normaliser les données en utilisant des méthodes de normalisation de données telles que df.apply() ou df.map()
7. Enregistrer les données nettoyées en utilisant la méthode df.to_csv() ou df.to_excel() pour les utiliser ultérieurement.

## License

### Ce projet est sous license MIT. Veuillez vous référer au fichier LICENSE pour plus d'informations.
