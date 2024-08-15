from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class LogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'log'
    verbose_name = _("System Logs")

    def ready(self):
        import log.signals
