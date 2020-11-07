from django.http import Http404

from rest_framework.response import Response
from rest_framework import viewsets

class SingletonViewSet(viewsets.ModelViewSet):

	# list is same as retrieve
    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # map update and create to new update function
    def create(self, request, *args, **kwargs):
    	return self.update_or_create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
    	return self.update_or_create(request, *args, **kwargs)

    # update or create the object
    def update_or_create(self, request, *args, **kwargs):
    	obj = self.get_singleton_object_or_none(request, *args, **kwargs)
    	serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update_or_create(request, serializer, *args, **kwargs)
        return Response(serializer.data)

    def perform_update_or_create(self, request, serializer, *args, **kwargs):
        serializer.save()

    # retrieve single object
    def retrieve(self, request, *args, **kwargs):
    	obj = self.get_singleton_object_or_404(request, *args, **kwargs)
        self.check_object_permissions(self.request, obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    # needs to be implemented
    def get_singleton_object_or_404(self, request, *args, **kwargs):
    	try:
    		return self.get_singleton_object(request, *args, **kwargs)
    	except self.model.DoesNotExist:
    		raise Http404

    def get_singleton_object_or_none(self, request, *args, **kwargs):
    	try:
    		return self.get_singleton_object(request, *args, **kwargs)
    	except self.model.DoesNotExist:
    		return None

    def get_singleton_object(self, request, *args, **kwargs):
    	raise