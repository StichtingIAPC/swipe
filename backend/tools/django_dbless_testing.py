from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation. This can be used when doing tests that do not communicate
     with the database. Select this particular class as runner (tools.DjangoDBLessTesting.NoDbTestRunner) when you want
     to skip waiting for DB migration."""

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass
