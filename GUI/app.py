from flask import Flask, render_template, request

from sys import path
path.append('../recommender_algorithm')
import user_recommendation as recommender

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        base = request.form.get('base')
        client = request.form.get('client')
        libelle = request.form.get('libelle')
        nb_art = request.form.get('nb_art')
        filtered = request.form.get('filtered')

        client = int(client) if client != '' else 0
        nb_art = int(nb_art) if nb_art != '' else 1
        result = []
        if base == 'base1':
            is_filtered = True if filtered else False
            result = ur.client_based_recommendation(client, nb_art, is_filtered)
            if is_filtered:
                pref_f, pref_u, pref_m, month = ur.get_user_preferences(client)
                return render_template('response.html', result=result, client=client, pref_f=pref_f, pref_u=pref_u, pref_m=pref_m, month=month)
            return render_template('response.html', result=result, client=client)
        elif base == 'base2':
            result = ur.item_based_recommendation(libelle, nb_art)
            return render_template('response.html', result=result, libelle=libelle)

        return render_template('response.html', result=result)

    return render_template('form.html')

if __name__ == '__main__':
    app.logger.info("Initializing dataset...")
    ur = recommender.UserRecommendation()
    app.run(host='127.0.0.1', port=8000)