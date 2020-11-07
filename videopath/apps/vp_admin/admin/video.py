from django.contrib import admin

from .base import VideopathModelAdmin

from ..models import  Video

#
# Video Admin
#
class VideoAdmin(VideopathModelAdmin):

	only_superusers = False

	list_display = ('key','created', 'player_version', 'team', 'title','total_plays')
	list_filter = ['player_version',]
	search_fields = ['draft__title', 'key', 'team__owner__username']
	ordering = ('-created',)

	actions=["make_export_jpgs"]


	def title(self,obj):
		return obj.draft.title

	def make_export_jpgs(self, request,queryset):
	    for video in queryset.all():
	        status, result = video.export_jpg_sequence()
	        self.message_user(request, result)

	make_export_jpgs.short_description = "Export JPGs"

admin.site.register(Video, VideoAdmin)