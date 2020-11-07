from django.contrib import admin

from videopath.apps.files.models import ImageFile


class ImageFileAdmin(admin.ModelAdmin):
    list_display = ('key', 'created', 'status')
admin.site.register(ImageFile, ImageFileAdmin)
