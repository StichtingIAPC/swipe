from django.apps import AppConfig


class SupplicationConfig(AppConfig):
    name = 'supplication'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import supplication.signals.handlers
