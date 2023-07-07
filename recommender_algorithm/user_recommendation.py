# dataframe manipulation
import numpy as np
import pandas as pd

# vectorization
from sklearn.preprocessing import LabelEncoder, StandardScaler

# cosine similarity
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
import numpy as np

# system
from sys import exit as sysexit
import statistics
from copy import deepcopy
from datetime import datetime

class UserRecommendation:
    def __init__(self):
        # import original dataset
        self.df = pd.read_csv("../datasets/KaDo.csv", sep=",")
        self.vec_df = self.df.reindex(columns=['CLI_ID', 'MOIS_VENTE', 'PRIX_NET', 'FAMILLE', 'UNIVERS', 'MAILLE', 'LIBELLE'])
        self.encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.base_recommendation = pd.DataFrame()

    def vectorize_dataframe(self, libelle=False):
        # vectorize / hash text variables
        self.vec_df["FAMILLE"] = self.encoder.fit_transform(self.vec_df["FAMILLE"])
        self.vec_df["UNIVERS"] = self.encoder.fit_transform(self.vec_df["UNIVERS"])
        self.vec_df["MAILLE"] = self.encoder.fit_transform(self.vec_df["MAILLE"])
        if libelle:
            self.vec_df["LIBELLE_CLEAR"] = self.vec_df["LIBELLE"]
        self.vec_df["LIBELLE"] = self.vec_df["LIBELLE"].apply(hash)

        # normalize every variables
        self.vec_df[["MOIS_VENTE", "PRIX_NET", "FAMILLE", "UNIVERS", "MAILLE", "LIBELLE"]] = self.scaler.fit_transform(self.vec_df[["MOIS_VENTE", "PRIX_NET", "FAMILLE", "UNIVERS", "MAILLE", "LIBELLE"]])

    def reset_variables(self):
        self.vec_df = self.df.reindex(columns=['CLI_ID', 'MOIS_VENTE', 'PRIX_NET', 'FAMILLE', 'UNIVERS', 'MAILLE', 'LIBELLE'])
        self.encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.base_recommendation = pd.DataFrame()

    def client_based_recommendation(self, cli_id, nb_articles=1, filter_by_columns=False):
        # reset required variables
        self.reset_variables()
        # vectorize and normalize variables
        self.vectorize_dataframe()
        # get the 5 most similar product depending client's previous purchases
        client_purchases = self.vec_df[self.vec_df['CLI_ID'] == cli_id]
        if client_purchases.empty:
            return "Client not found"
        other_purchases = self.vec_df[self.vec_df['CLI_ID'] != cli_id]
        similarities = cosine_similarity(client_purchases, other_purchases)
        top_indices = similarities.argsort()[:, -nb_articles:]

        # format output items and similarities in a single dataframe
        similarities_percentages = []
        self.base_recommendation = pd.DataFrame()
        for elem, i in zip(top_indices, range(len(top_indices))):
            self.base_recommendation = pd.concat([self.base_recommendation, self.df.iloc[elem]])
            top_articles = self.df.iloc[elem]['LIBELLE'].tolist()
            for line, n in zip(top_articles, range(len(top_articles))):
                similarities_percentages.append(str(similarities[i][top_indices[i]][n]))
        self.base_recommendation['SIMIL'] = similarities_percentages

        # call apply_user_preferences if any of p_family p_universe or p_maille is true
        if filter_by_columns:
            filtered_recommendation = self.apply_user_preferences(cli_id)
            return filtered_recommendation.head(nb_articles).values.tolist()
        else:
            self.base_recommendation.sort_values(by=['SIMIL', 'PRIX_NET'])
            return self.base_recommendation.head(nb_articles).values.tolist()

    def get_user_preferences(self, cli_id):
        # client's preferences depending on its purchase history
        current_month = datetime.now().month
        current_month_df = self.df.loc[((self.df['CLI_ID'] == cli_id) & (self.df['MOIS_VENTE'] == current_month))]
        # use purchases made at current time of year if available, otherwise use every purchases
        input_df = current_month_df if not current_month_df.empty else self.df[self.df['CLI_ID'] == cli_id]

        prefered_families = input_df["FAMILLE"].value_counts().index.to_list()
        prefered_universes = input_df["UNIVERS"].value_counts().index.to_list()
        prefered_mailles = input_df["MAILLE"].value_counts().index.to_list()

        if current_month_df.empty:
            return prefered_families, prefered_universes, prefered_mailles, None
        return prefered_families, prefered_universes, prefered_mailles, datetime.now().strftime("%B")

    def apply_user_preferences(self, cli_id):
        # client's preferences depending on its purchase history
        current_month = datetime.now().month
        current_month_df = self.df.loc[((self.df['CLI_ID'] == cli_id) & (self.df['MOIS_VENTE'] == current_month))]
        # use purchases made at current time of year if available, otherwise use every purchases
        input_df = current_month_df if not current_month_df.empty else self.df[self.df['CLI_ID'] == cli_id]

        prefered_families = input_df["FAMILLE"].value_counts().index.to_list()
        prefered_universes = input_df["UNIVERS"].value_counts().index.to_list()
        prefered_mailles = input_df["MAILLE"].value_counts().index.to_list()
        filtered_articles = self.base_recommendation.loc[(
            (self.base_recommendation['UNIVERS'].isin(prefered_families)) |
            (self.base_recommendation['FAMILLE'].isin(prefered_universes)) |
            (self.base_recommendation['MAILLE'].isin(prefered_mailles))
        )]
        # filter articles based on high similarity and low price
        filtered_articles.sort_values(by=['SIMIL', 'PRIX_NET'])

        return filtered_articles

    def item_based_recommendation(self, libelle, nb_articles=1):
        # reset required variables
        self.reset_variables()
        # vectorize and normalize variables
        self.vectorize_dataframe(True)
        # get the 5 most similar product depending on input item
        article = deepcopy(self.vec_df[self.vec_df['LIBELLE_CLEAR'] == libelle])
        if article.empty:
            return "Article not found"
        other_articles = deepcopy(self.vec_df[self.vec_df['LIBELLE_CLEAR'] != libelle])
        # drop temporary column used to retrieve article by libelle
        article.drop(['LIBELLE_CLEAR'], axis=1, inplace=True)
        other_articles.drop(['LIBELLE_CLEAR'], axis=1, inplace=True)
        similarities = cosine_similarity(article.head(20), other_articles)
        top_indices = similarities.argsort()[:, -nb_articles:]

        # format output items and similarities in a single dataframe
        similarities_percentages = []
        base_recommendation = pd.DataFrame()
        for elem, i in zip(top_indices, range(len(top_indices))):
            base_recommendation = pd.concat([base_recommendation, self.df.iloc[elem]])
            top_articles = self.df.iloc[elem]['LIBELLE'].tolist()
            for line, n in zip(top_articles, range(len(top_articles))):
                similarities_percentages.append(str(similarities[i][top_indices[i]][n]))
        base_recommendation['SIMIL'] = similarities_percentages
        base_recommendation.sort_values(by=['SIMIL', 'PRIX_NET'])

        return base_recommendation.head(nb_articles).values.tolist()
