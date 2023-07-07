import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

print("Load csv ...")
df = pd.read_csv("/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/datasets/KaDo.csv", sep=",")
print("Extract to csv file")
size_df = len(df.index)
print("Base dataframe has", size_df, "rows.")

### Nettoyage des données

# Suppression des lignes possédants des données NULL
na_free = df.dropna()
only_na = df[~df.index.isin(na_free.index)]
df = df.dropna()
print(len(only_na.index), "rows dropped with empty values")

# Vérifier les lignes en double, et supprimer les lignes identitques
duplicated_rows = df.duplicated()
print("DUP:",duplicated_rows.sum())

### Cleaning outliers
# Calculating mean value of each product (grouped by LIBELLE column)
mean_price = df.groupby("LIBELLE")["PRIX_NET"].mean()

# Creating a new column with the mean price of each product
df["mean_price"] = df["LIBELLE"].apply(lambda x: mean_price[x])

# Finding rows with abnormal prices (more than 3 times the mean price)
abnormal_rows = df[df["PRIX_NET"] > 3 * df["mean_price"]]

# Removing rows with abnormal prices
df = df[~df.index.isin(abnormal_rows.index)]

# Printing number of rows after cleaning
print("Number of rows after cleaning:", len(df))


# Number of items by FAMILLE / UNIVERS / MAILLE

df["FAMILLE"].value_counts().to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/famille_occurence.csv')
df["UNIVERS"].value_counts().to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/univers_occurence.csv')
df["MAILLE"].value_counts().to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/maille_occurence.csv')

# Popular item by FAMILLE / UNIVERS / MAILLE

df_popular_famille = df.groupby("FAMILLE")["LIBELLE"].value_counts().reset_index(name="occurence")[["FAMILLE","LIBELLE","occurence"]].groupby("FAMILLE").apply(lambda x: x.nlargest(1,'occurence'))
df_popular_univers = df.groupby("UNIVERS")["LIBELLE"].value_counts().reset_index(name="occurence")[["UNIVERS","LIBELLE","occurence"]].groupby("UNIVERS").apply(lambda x: x.nlargest(1,'occurence'))
df_popular_maille = df.groupby("MAILLE")["LIBELLE"].value_counts().reset_index(name="occurence")[["MAILLE","LIBELLE","occurence"]].groupby("MAILLE").apply(lambda x: x.nlargest(1,'occurence'))
df_popular_famille.to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/popular_item_famille.csv')
df_popular_univers.to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/popular_item_univers.csv')
df_popular_maille.to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/popular_item_maille.csv')

# Mean price by FAMILLE / UNIVERS / MAILLE

df.groupby('FAMILLE')['PRIX_NET'].mean().to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/price_mean_famille.csv')
df.groupby('UNIVERS')['PRIX_NET'].mean().to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/price_mean_univers.csv')
df.groupby('MAILLE')['PRIX_NET'].mean().to_csv('/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/price_mean_maille.csv')

# Mean sold items by FAMILLE / UNIVERS / MAILLE

df.groupby(['CLI_ID', 'FAMILLE']).size().reset_index(name='counts').groupby(['FAMILLE']).mean().reset_index().to_csv("/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/sold_mean_famille.csv")
df.groupby(['CLI_ID', 'UNIVERS']).size().reset_index(name='counts').groupby(['UNIVERS']).mean().reset_index().to_csv("/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/sold_mean_univers.csv")
df.groupby(['CLI_ID', 'MAILLE']).size().reset_index(name='counts').groupby(['MAILLE']).mean().reset_index().to_csv("/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/sold_mean_maille.csv")

# Mean sold item for ticket ID by FAMILLE / UNIVERS / MAILLE

df.groupby(['TICKET_ID', 'FAMILLE']).size().reset_index(name='counts').groupby(['FAMILLE']).mean().reset_index().to_csv("/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/ticket_mean_famille.csv")
df.groupby(['TICKET_ID', 'UNIVERS']).size().reset_index(name='counts').groupby(['UNIVERS']).mean().reset_index().to_csv("/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/ticket_mean_univers.csv")
df.groupby(['TICKET_ID', 'MAILLE']).size().reset_index(name='counts').groupby(['MAILLE']).mean().reset_index().to_csv("/Users/halilbagdadi/Documents/Epitech/recommender/T-DAT-901-LYO_19/DATA_EXPLORATION/DATA_VISUALISATION/ticket_mean_maille.csv")

# Mean sold item for ticket ID by FAMILLE / UNIVERS / MAILLE"1490281"

id_client = 13290776
id_month = 12

df.loc[df['CLI_ID'] == id_client].reset_index() # Loc sur le id_client 
df.loc[(df['CLI_ID'] == id_client)].groupby('MOIS_VENTE')['PRIX_NET'].mean().reset_index() # Df contenant la moyenne d'argent dépensés par mois
df.loc[(df['CLI_ID'] == id_client)].groupby('MOIS_VENTE').size().reset_index(name='COMMANDES') # Df contenant le nombre de commandes moyennes par mois

# Df contenant les 3 FAMILLE préférés pour id_client & id_month
df_filtered = df.loc[(df['CLI_ID'] == id_client) & (df['MOIS_VENTE'] == id_month)].groupby(['FAMILLE']).size().reset_index(name='COMMANDES')
familles_recurrentes = df_filtered.nlargest(3, 'COMMANDES')[['FAMILLE']]
print(familles_recurrentes)

# Df contenant les 3 UNIVERS préférés pour id_client & id_month
df_filtered = df.loc[(df['CLI_ID'] == id_client) & (df['MOIS_VENTE'] == id_month)].groupby(['UNIVERS']).size().reset_index(name='COMMANDES')
familles_recurrentes = df_filtered.nlargest(3, 'COMMANDES')[['UNIVERS']]
print(familles_recurrentes)

# Df contenant les 3 MAILLE préférés pour id_client & id_month
df_filtered = df.loc[(df['CLI_ID'] == id_client) & (df['MOIS_VENTE'] == id_month)].groupby(['MAILLE']).size().reset_index(name='COMMANDES')
familles_recurrentes = df_filtered.nlargest(3, 'COMMANDES')[['MAILLE']]
print(familles_recurrentes)

# Df contenant les 3 LIBELLE préférés pour id_client & id_month
df_filtered = df.loc[(df['CLI_ID'] == id_client) & (df['MOIS_VENTE'] == id_month)].groupby(['LIBELLE']).size().reset_index(name='COMMANDES')
familles_recurrentes = df_filtered.nlargest(3, 'COMMANDES')[['LIBELLE']]
print(familles_recurrentes)