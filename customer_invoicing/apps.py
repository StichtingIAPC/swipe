from django.apps import AppConfig


class CustomerInvoicingConfig(AppConfig):
    name = 'customer_invoicing'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import customer_invoicing.signals.handlers

