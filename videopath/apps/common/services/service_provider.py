import importlib

from django.conf import settings

PACKAGE = "videopath.apps.common.services."

def get_service(name):
	name = PACKAGE + name + "_service"

	if settings.SERVICE_MOCKS:
		name += "_mock"

	module = importlib.import_module(name)
	return module