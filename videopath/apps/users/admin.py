from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from .models import APIToken, UserCampaignData, UserSalesInfo, AuthenticationToken,UserActivityDay, OneTimeAuthenticationToken, UserActivity, AutomatedMail, UserSettings, User, Team, TeamMember
from videopath.apps.users.actions import move_user_to_pipedrive


class UserAdmin(_UserAdmin):
    list_display = (
        'pk', 'username', 'email', 'videos_link', 'date_joined', 'last_login')
    ordering = ('-date_joined',)
    search_fields = ['username', 'email']

    def videos_link(self, obj):
        from videopath.apps.videos.models import Video
        link = "/admin/videos/video/?team__owner__username=" + obj.username
        return "<a href = '" + link + "'>List of Videos</a> (" + str(Video.objects.filter(team__owner_id = obj.pk).count()) + ")"
    videos_link.allow_tags = True
    
    actions=["make_move_to_pipedrive"]
    def make_move_to_pipedrive(self, request, queryset):
        for user in queryset.all():
            move_user_to_pipedrive.run(user)
    make_move_to_pipedrive.short_description = "Move to pipedrive"


class TeamAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'owner', 'is_default_team_of_user')
    search_fields = ['owner__username', 'owner__email', 'name']

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role')
    search_fields = ['user__username', 'user__email']

class UserSalesInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'pipedrive_person_id')


class UserSettingsAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_seen')
    ordering = ('-last_seen',)
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }
    

class UserActivityDayAdmin(admin.ModelAdmin):
    list_display = ('user', 'day')
    ordering = ('-day',)
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


class AutomatedMailAdmin(admin.ModelAdmin):
    list_display = ('user', 'mailtype', 'created')
    search_fields = ['user__email', 'user__username', 'mailtype']
    ordering = ('-created',)
    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created', 'last_used')
    fields = ('user',)
    ordering = ('-last_used',)
    raw_id_fields = ['user',]
    search_fields = ['user__username', 'user__email']

    autocomplete_lookup_fields = {
        'fk': ['user',],
    }

class OTTokenAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email']

    list_display = ('key', 'created')
    #fields = ('key',)
    ordering = ('created',)

class UserCampaignDataAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email']
    list_display = ('user', 'created')
    ordering = ('created',)

class APITokenAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email']
    list_display = ('user', 'created', 'key')

#admin.site.unregister(User)
admin.site.unregister(UserSettings)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(AuthenticationToken, TokenAdmin)
admin.site.register(OneTimeAuthenticationToken, OTTokenAdmin)
admin.site.register(UserActivity, UserActivityAdmin)
admin.site.register(UserActivityDay, UserActivityDayAdmin)
admin.site.register(UserCampaignData, UserCampaignDataAdmin)
admin.site.register(UserSalesInfo, UserSalesInfoAdmin)
admin.site.register(APIToken, APITokenAdmin)

admin.site.register(AutomatedMail, AutomatedMailAdmin)
admin.site.register(UserSettings, UserSettingsAdmin)


