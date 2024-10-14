from django.apps import AppConfig


class ReviewManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'review_management'

    def ready(self):
        import review_management.signals