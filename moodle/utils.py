import requests
from time import time
from decouple import config

MOODLE_API_URL = config('MOODLE_API_URL')  # Récupérer l'URL de l'API depuis le fichier .env
MOODLE_API_TOKEN = config('MOODLE_API_TOKEN')  # Récupérer la clé API

url=MOODLE_API_URL
def call_moodle_api(url, token, function_name):
    """
    Fonction pour appeler une API Moodle avec le token et la fonction spécifiée.
    """
    function_name="core_user_get_users"
    api_url = f"{url}/webservice/rest/server.php"
    params = {
        'wstoken': token,
        'wsfunction': function_name,
        'moodlewsrestformat': 'json'
    }

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()  # Retourne les données JSON de Moodle
    else:
        return {"error": "Failed to fetch data from Moodle API"}

def get_connected_users(url, token):
    """
    Récupère les utilisateurs qui sont actuellement connectés.
    """
    criteria = [
        {
            'key': 'lastaccess',
            'value': time(),  # Heure actuelle
            'operator': '>',
        }
    ]
    
    data = call_moodle_api(
        url=url,
        token=token,
        function_name="core_user_get_users",
        criteria=criteria,
        fields=['firstname', 'lastname', 'email', 'lastaccess']
    )
    
    return data


def fetch_users_from_moodle():
    params = {
        'wstoken': MOODLE_API_TOKEN,  # Utilisation de la clé API
        'wsfunction': 'core_user_get_users',  # Fonction API pour récupérer les utilisateurs
        'moodlewsrestformat': 'json',  # Format des données (ici en JSON)
        'criteria[0][key]': 'lastaccess',  # Critère de recherche
        'criteria[0][value]': 0,  # Valeur du critère
    }
    response = requests.get(MOODLE_API_URL, params=params)
    response.raise_for_status()  # Lancer une erreur si la requête échoue
    return response.json()['users']  # Retourner les utilisateurs récupérés
