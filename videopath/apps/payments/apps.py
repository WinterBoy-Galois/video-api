from django.apps import AppConfig

class PaymentsConfig(AppConfig):
	name = 'videopath.apps.payments'
	def ready(self):
		import model_extensions
		import signals_receiver