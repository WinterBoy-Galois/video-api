from django.core.management.base import BaseCommand

from videopath.apps.analytics.services import ga_import_service

class Command(BaseCommand):

    def handle(self, *args, **options):
    	start = 0 if not len(args) else int(args[0])
        ga_import_service.import_historical_data(start)
