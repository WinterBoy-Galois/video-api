from django.apps import AppConfig

class FilesConfig(AppConfig):
	name = 'videopath.apps.files'
	def ready(self):
		import signals_receiver