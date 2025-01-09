# tasks.py
from celery import shared_task
from decouple import config
from moodle.utils import call_moodle_api
from moodle.utils import get_connected_users
from moodle.models import MoodleUser
import logging
from moodle.utils import fetch_users_from_moodle

MOODLE_API_URL = config('MOODLE_API_URL')  
MOODLE_API_TOKEN = config('MOODLE_API_TOKEN')

@shared_task
def fetch_moodle_data_task():
    """
    Cette tâche va récupérer les données depuis l'API Moodle de la plateforme unique.
    Les informations de la plateforme Moodle sont directement dans settings.py.
    """
    try:
        # Accéder aux paramètres définis dans le fichier env
        url = MOODLE_API_URL
        token = MOODLE_API_TOKEN
        
        # Appel de l'API Moodle pour obtenir des informations sur le site
        data = call_moodle_api(
            url=url,
            token=token,
            function_name="core_user_get_users"  
        )
        print(f"Data retrieved from Moodle: {data}")
        return data
    except Exception as e:
        print(f"Error retrieving data from Moodle: {str(e)}")
        return None

logger = logging.getLogger(__name__)

@shared_task
def fetch_and_save_users():
    users = fetch_users_from_moodle()  # Fonction qui récupère les utilisateurs
    if not users:
        logger.warning("Aucun utilisateur récupéré depuis Moodle.")
    for user_data in users:
        user, created = MoodleUser.objects.update_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'full_name': user_data['fullname'],
                'last_login': user_data['lastaccess'],
            },
        )
        if created:
            logger.info(f"Utilisateur {user_data['username']} créé.")
        else:
            logger.info(f"Utilisateur {user_data['username']} mis à jour.")
    return len(users)
