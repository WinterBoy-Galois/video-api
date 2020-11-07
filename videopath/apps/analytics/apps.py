from django.apps import AppConfig

class AnalyticsConfig(AppConfig):
	name = 'videopath.apps.analytics'
	def ready(self):
		import signals_receiver