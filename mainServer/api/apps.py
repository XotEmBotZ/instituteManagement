from django.apps import AppConfig
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        super().ready()
        if os.environ.get('RUN_MAIN', None) != 'true':
            from . import bgJobs
            bgJobs.run_continuously()