from django.apps import AppConfig

class VideosConfig(AppConfig):
	name = 'videopath.apps.videos'
	def ready(self):
		import signals_receiver
		import services_receiver