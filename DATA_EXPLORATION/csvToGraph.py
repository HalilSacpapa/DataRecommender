#!/usr/bin/env python3

import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os

# Chemin du dossier contenant les fichiers CSV
folder_path = '/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/'
# conn_string = 'postgresql://postgres:postgres@localhost/postgres'
conn_string = 'postgresql://postgres:postgres@localhost:5432/postgres'

# Pour chaque fichier dans le dossier
for filename in os.listdir(folder_path):
    # Si le fichier a l'extension .csv
    if filename.endswith(".csv"):
        # Charger le fichier en utilisant pandas
        df = pd.read_csv(folder_path + filename)
        # Afficher le nom du fichier
        print("Importing dataframes", filename, "to sql database ...")
        db = create_engine(conn_string)
        conn = db.connect()
        df.to_sql(filename[:-4], con=conn, if_exists='replace', index=True)
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        conn.close()
        print("Dataframes", filename[:-4], "imported succesfully !!!")