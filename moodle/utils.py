import requests
from time import time
from decouple import config
import logging

logger = logging.getLogger(__name__)

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
    try:
        logger.info('Démarrage de la récupération des utilisateurs depuis Moodle.')
        params = {
            'wstoken': MOODLE_API_TOKEN,
            'wsfunction': 'core_user_get_users',
            'moodlewsrestformat': 'json',
            'criteria[0][key]': 'lastaccess',
            'criteria[0][value]': 0,
        }
        response = requests.get(MOODLE_API_URL, params=params)
        response.raise_for_status()  # Si une erreur survient, elle sera levée ici
        users = response.json()['users']
        logger.info(f"{len(users)} utilisateurs récupérés.")
        print(users)  # Pour vérifier directement les utilisateurs récupérés
        return users
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la récupération des utilisateurs Moodle : {e}")
        raise
