from django.apps import apps
from django.core.management.base import BaseCommand

from factory_generator import utils


apps_configs = apps.get_app_configs()

class Command(BaseCommand):
    help = 'Fill database using data generated by factories in django apps'

    def handle(self, *args, **options):
        config = utils.load_config()
        for app in config.apps:
            app_config = apps.get_app_config(app)
            for factory in utils.get_app_factories(app_config.path):
                factory.create_batch(config.quantity)
                self.stdout.write(self.style.SUCCESS(f'Successfully created {config.quantity} \
                objects of model {factory._meta.model}'))