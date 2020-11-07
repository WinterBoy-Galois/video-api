from django.core.management.base import BaseCommand

from videopath.apps.analytics.services import ga_import_service


class Command(BaseCommand):

    def handle(self, *args, **options):
        ga_import_service.import_data()
