from flask import Flask, render_template, request
import pandas as pd

# Chargement des données depuis le fichier CSV
alerts_series = pd.read_csv('/Users/macbook/Desktop/_elamri_yassine_/exercice1/data_2023_06_15.csv')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Récupérer les coordonnées uniques disponibles dans le fichier CSV
    coordinates = alerts_series[['Latitude', 'Longitude']].drop_duplicates().values.tolist()

    return render_template('index.html', coordinates=coordinates)

@app.route('/show_location', methods=['POST'])
def show_location():
    # Récupérer les coordonnées sélectionnées par l'utilisateur
    selected_coordinates = request.form['coordinates'].split(',')

    # Convertir les coordonnées en nombres à virgule flottante
    latitude = float(selected_coordinates[0])
    longitude = float(selected_coordinates[1])

    # Rechercher les informations pour le point sélectionné dans le fichier CSV
    selected_point = alerts_series[(alerts_series['Latitude'] == latitude) & (alerts_series['Longitude'] == longitude)]

    if selected_point.empty:
        error_message = "Aucune information disponible pour le point sélectionné."
        return render_template('index.html', error_message=error_message, coordinates=selected_coordinates)

    commune = selected_point['departement'].values[0]
    phénomène = selected_point['Phénomène'].values.tolist()
    couleur = selected_point['Couleur'].values.tolist()

    return render_template('index.html', coordinates=selected_coordinates, selected_latitude=latitude, selected_longitude=longitude,
                           commune=commune, phénomène=phénomène, couleur=couleur)


#if __name__ == '__main__':
    #app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0')# rendre l'application accessible á tous hotspot 
