from pytest_factoryboy import register

from tests.factories import CategoryFactory, UserFactory, AdFactory

pytest_plugins = "test.fixtures"

register(CategoryFactory)
register(UserFactory)
register(AdFactory)
