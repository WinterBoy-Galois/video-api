from django.core.management.base import BaseCommand

import importlib

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('module')
        parser.add_argument('action')

    def handle(self, *args, **options):
    	
    	app_name = options['module']
    	action_name = options['action']
    	
    	print '\n\n'
    	print 'Running action ' + action_name + ' from app ' + app_name
    	print '==========================================\n'

    	path = 'videopath.apps.' + app_name + '.actions.' + action_name
    	action = importlib.import_module(path)

    	action.run()

    	


