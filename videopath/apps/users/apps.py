from django.apps import AppConfig

class UsersConfig(AppConfig):
	name = 'videopath.apps.users'
	def ready(self):
		import signals_receiver