from django.apps import AppConfig

class IntegrationsConfig(AppConfig):
	name = 'videopath.apps.integrations'
	def ready(self):
		pass
		#import signals_receiver