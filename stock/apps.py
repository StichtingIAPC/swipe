from django.apps import AppConfig


class StockConfig(AppConfig):
    name = 'stock'

    def ready(self):

        # noinspection PyUnresolvedReferences
        import stock.signals.handlers
