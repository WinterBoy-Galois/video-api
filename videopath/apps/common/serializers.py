from django.core.paginator import Paginator

from rest_framework import serializers
from rest_framework import pagination
#
#  Helper to get a paginated output of otherwise flat serilizer output
#
def get_paginated_serializer(objects, serializer_class, serializer_args = {}, page_size=20, page=1):
	page =  Paginator(objects, page_size).page(page)


	class PaginationSerializer(serializers.Serializer):
		"""
		A base class for pagination serializers to inherit from,
		to make implementing custom serializers more easy.
		"""
		results_field = 'results'
		count = serializers.ReadOnlyField(source='paginator.count')
		
		def __init__(self, *args, **kwargs):
		    """
		    Override init to add in the object serializer field on-the-fly.
		    """
		    super(PaginationSerializer, self).__init__(*args, **kwargs)
		    results_field = self.results_field

		    try:
		        list_serializer_class = serializer_class.Meta.list_serializer_class
		    except AttributeError:
		        list_serializer_class = serializers.ListSerializer

		    self.fields[results_field] = list_serializer_class(
		        child=serializer_class(page, **serializer_args),
		        source='object_list'
		    )

	return PaginationSerializer(page)