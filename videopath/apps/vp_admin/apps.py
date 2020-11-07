from django.apps import AppConfig

class AdminConfig(AppConfig):
	name = 'videopath.apps.vp_admin'
	def ready(self):
		pass
		#import signals_receiver