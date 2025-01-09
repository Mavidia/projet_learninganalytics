from moodle.tasks import fetch_and_save_users
from django.http import JsonResponse
from moodle.tasks import fetch_moodle_data_task
from moodle.utils import fetch_users_from_moodle

def fetch_data_for_moodle(request):
    """
    Lance la tâche Celery pour récupérer les données de la plateforme Moodle unique.
    """
    fetch_moodle_data_task.delay()  # Appelle la tâche en arrière-plan pour récupérer les données
    return JsonResponse({"success": True, "message": "Task started for Moodle"})

def fetch_users(request):
    """
    Récupère les utilisateurs directement sans utiliser Celery.
    """
    try:
        users = fetch_users_from_moodle()  # Récupère les utilisateurs depuis Moodle
        return JsonResponse({"success": True, "users": users})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

def trigger_fetch_users(request):
    print("La tâche a été lancée")
    fetch_and_save_users.delay()
    return JsonResponse({"success": True, "message": "Task started"})