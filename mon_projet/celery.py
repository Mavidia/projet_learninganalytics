
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab  # Importer la planification

# Définir le module de configuration Celery pour Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')

app = Celery('mon_projet')

# Charger la configuration depuis Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches asynchrones
app.autodiscover_tasks()

# Configuration de Celery Beat
app.conf.beat_schedule = {
    'fetch-moodle-data-every-hour': {
        'task': 'moodle.tasks.fetch_moodle_data_task',
        'schedule': crontab(minute=0, hour='*'),  # Chaque heure
    },
}



