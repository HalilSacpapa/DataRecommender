import user_recommendation as recommender

cli_id = 1490281
# cli_id = 21351166
# cli_id = 90822328
# cli_id = 126716008

libelle = "GLOSS SEXYPULP CRISTAL 08 CN3 10ML"
# libelle = "CD JDM4 MACADAMIA FL 200ML"
# libelle = "GEL DOUCHE FRAICHEUR VETIVER 200ML"
# libelle = "SVC PIEDS CR DEO 12H T50ML"
# libelle = "GEL NETT HYDRA VEG T125ML"
# libelle = "CREME MAINS T75 ml FRUITS ROUGES"
# libelle = "LAIT DEMAQ 2010 SV FL200ML"
# libelle = "PORTE MINE VERT 03 CN3 0.3G"
# libelle = "GM 200ml FRUITS ROUGES"
# libelle = "BAUME LEVRES VANILLE 4G"

print("Initializing dataset...")
ur = recommender.UserRecommendation()
while True:
    reco = input("\nType 'user' for user-based recommendation or 'item' for item-based recommendation: ")
    if reco == 'user':
        cli_id = int(input("Enter a client id: "))
        if cli_id == '':
            print("Client ID is required")
            continue
        nb_art = input("Enter the number of articles to recommend (default = 1): ")
        nb_art = int(nb_art) if nb_art != '' else 1
        col_filter = input("Filter by columns? (y/n): ")
        filter_by_columns = True if col_filter == 'y' else False
        print("Processing...")
        print(ur.client_based_recommendation(cli_id, nb_art, filter_by_columns))
    elif reco == 'item':
        libelle = input("Enter an article name: ")
        if libelle == '':
            print("Article name is required")
            continue
        nb_art = input("Enter the number of articles to recommend (default = 1): ")
        nb_art = int(nb_art) if nb_art != '' else 1
        print("Processing...")
        print(ur.item_based_recommendation(libelle, nb_art))