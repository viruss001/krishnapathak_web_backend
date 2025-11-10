from django.apps import AppConfig


class PoliciesConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = "policy"

    def ready(self):
        # ensure signals are registered
        from . import signals  # noqa: F401
