from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    label= 'my_account'
    def ready(self):
        from . import signals