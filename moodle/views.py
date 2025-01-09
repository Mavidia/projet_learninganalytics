
from django.http import JsonResponse
from .tasks import fetch_moodle_data_task

def fetch_data_for_moodle(request):
    """
    Lance la tâche Celery pour récupérer les données de la plateforme Moodle unique.
    """
    fetch_moodle_data_task.delay()  # Appelle la tâche en arrière-plan pour récupérer les données
    return JsonResponse({"success": True, "message": "Task started for Moodle"})

