from django.conf import settings

import configparser
from factory.django import DjangoModelFactory
import os
from typing import NamedTuple, List


BASE_DIR = settings.BASE_DIR
FACTORIES_MODULE_NAME = 'factories'


class Config(NamedTuple):
    apps: List[str]
    quantity: int


def get_config_path() -> str:
    return os.path.join(BASE_DIR, 'factory_generator.ini')


def load_config() -> Config:
    """
    Return Config object
    """
    config = configparser.ConfigParser()
    config.read(get_config_path())
    apps = config['factory_generator']['apps'].split(sep=',')
    quantity = int(config['factory_generator']['quantity'])
    return Config(apps=apps, quantity=quantity)


def import_factories_module(file_path: str):
    """
    Import factories.py module by path

def get_factories(app_path: str) -> List[DjangoModelFactory]:
    """
    Return list of instances of DjangoModelFactory.
    :param app: Filesystem path to the django application directory.
    """
    file_path = os.path.join(BASE_DIR, f'{FACTORIES_MODULE_NAME}.py')
    spec = importlib.util.spec_from_file_location(FACTORIES_MODULE_NAME, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
