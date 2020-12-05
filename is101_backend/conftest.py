from rest_framework.test import APIClient

import factory
import pytest


pytest_plugins = [
    "accounts.tests.fixtures",
    "company.tests.fixtures"
]

@pytest.fixture
def api_client():
   return APIClient()


@pytest.fixture
def factory_as_dict():
    # FIXME Обработать подфабрики
    def create_dict(factory_class, fields=None):
        """
        Генерирует словарь с атрибутами на основе класса фабрики.
        Если атрибут задается как подфабрика, то он не будет представлен словарем.
        :param factory_class: Класс фабрики
        :param fields: Список полей фабрики, которые нужно включить в словарь
        """
        factory_dict = factory.build(dict, FACTORY_CLASS=factory_class)
        if fields:
            result = {}
            for f in fields:
                result[f] = factory_dict[f]
            return result
        return factory_dict
    return create_dict
