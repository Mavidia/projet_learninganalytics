from __future__ import absolute_import, unicode_literals

# Cela assure que l'application Celery est chargée lorsque Django démarre.
from mon_projet.celery import app as celery_app

__all__ = ('celery_app',)
