
from django.contrib import admin

from .models import Integration

#
# Video
#
class IntegrationAdmin(admin.ModelAdmin):

    # fields
    list_display = ('team', 'service')
    ordering = ('-created',)
    search_fields = ['team', 'team__owner', 'service']

    


admin.site.register(Integration, IntegrationAdmin)


