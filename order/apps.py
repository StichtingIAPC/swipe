from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'order'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import order.signals.handlers
