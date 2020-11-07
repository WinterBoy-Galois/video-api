from django.db.models import Count
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .base import VideopathModelAdmin


from ..models import User, Video
from urlparse import urlparse

from videopath.apps.payments.actions import start_trial, downgrade_to_free_plan
from videopath.apps.users.actions import move_user_to_pipedrive

PIPEDRIVE_PERSON_URL = 'https://videopath.pipedrive.com/person/'




#
# User Filter
#
class PlanFilter(SimpleListFilter):
    title = 'plan' # or use _('country') for translated title
    parameter_name = 'plan'

    def lookups(self, request, model_admin):
        return [
        	('free', 'Free'),
        	('nonfree', 'Non Free')
        ]
        # You can also use hardcoded model name like "Country" instead of 
        # "model_admin.model" if this is not direct foreign key filter

    def queryset(self, request, queryset):
    	value = self.value()
        if value == 'free':
            return queryset.filter(subscription__plan='free-free')
        elif value == 'nonfree':
        	return queryset.exclude(subscription__plan='free-free').exclude(subscription=None)
        else:
            return queryset


#
# Sales user
#
class UserAdmin(VideopathModelAdmin):

	only_superusers = False

	#
	# Query set
	#
	def get_queryset(self, request):
		return User.objects.annotate(videos_count=Count('owned_teams__videos'))

	#
	# List display
	#
	def plan(self, obj):
		try:
			plan = obj.subscription.plan
		except:
			return 'free-free'
		status = ''
		try:
			status = 'switches to {0} on {1}'.format(obj.pending_subscription.plan, obj.subscription.current_period_end)
		except: 	
			if obj.subscription.current_period_end:
				status = 'renews {0}'.format(obj.subscription.current_period_end)

		return "{0}<br />{1}".format(plan, status)
	plan.admin_order_field = 'subscription__plan'
	plan.allow_tags = True
    
	def country(self, obj):
		try: return obj.campaign_data.country
		except: return '-'
	country.admin_order_field = 'campaign_data__country'

	def phone(self,obj):
		try: return obj.settings.phone_number
		except: return '-'


	def videos(self,obj):
		unpublished = Video.objects.filter(team__owner=obj, archived=False, published=False).count() 
		archived = Video.objects.filter(team__owner=obj, archived=True).count() 
		published = Video.objects.filter(team__owner=obj, archived=False, published=True).count() 
		return 'tot:' + str(obj.videos_count) + ' pub:' + str(published) + ' unp:' + str(unpublished) + ' arch:' + str(archived)
	videos.admin_order_field ='videos_count'

	def referrer(self,obj):
		try: url = obj.campaign_data.referrer
		except: return '-'
		if url:
		    parsed_uri = urlparse( url )
		    return '<a href="' + url + '">' + parsed_uri.netloc +'</a><br />';
		return '-'
	referrer.allow_tags=True

	def retention_mails(self,obj):
		return obj.settings.receive_retention_emails
	retention_mails.admin_order_field ='settings__receive_retention_emails'


	def pipedrive(self,obj):
		try:
			pid = obj.sales_info.pipedrive_person_id
			return '<a href="{0}">{1}</a>'.format(PIPEDRIVE_PERSON_URL + str(pid), pid)
		except:
			return '-'
	pipedrive.allow_tags=True

	def email_link(self, obj):
		return '<a href ="/admin/insights/users/{0}/">{0}</a>'.format(obj.email)
	email_link.admin_order_field = 'email'
	email_link.allow_tags=True

	list_display = (
	        'email_link', 
	        'date_joined',
	        'country',
	        'phone',
	        'referrer',
	        'plan',
	        'videos',
	        'pipedrive',
	        'retention_mails')

	#
	# Actions
	#
	actions=["make_toggle_retention_mails", "make_trial_2_weeks", "make_trial_4_weeks", "make_downgrade_to_free", "make_move_to_pipedrive"]

	def make_trial_2_weeks(self, request, queryset):
		for user in queryset.all():
			result = start_trial.run(user, 2)
			if not result: self.message_user(request, "Could not start trial. User {0} was not on the free plan!".format(user))

	make_trial_2_weeks.short_description = "2 Weeks Trial"

	def make_trial_4_weeks(self, request, queryset):
		for user in queryset.all():
			result = start_trial.run(user, 4)
			if not result: self.message_user(request, "Could not start trial. User {0} was not on the free plan!".format(user))

	make_trial_4_weeks.short_description = "4 Weeks Trial"


	def make_toggle_retention_mails(self, request, queryset):
	    for user in queryset.all():
		    user.settings.receive_retention_emails = not user.settings.receive_retention_emails
		    user.settings.save()
	make_toggle_retention_mails.short_description = "Toggle Retention mails"

	def make_downgrade_to_free(self, request, queryset):
		for user in queryset.all():
		    downgrade_to_free_plan.run(user)
	make_downgrade_to_free.short_description = "Downgrade to free plan"

	def make_move_to_pipedrive(self, request, queryset):
		for user in queryset.all():
			move_user_to_pipedrive.run(user)
	make_move_to_pipedrive.short_description = "Send user to pipedrive"

    	
	#
	# Filter & Search
	#
	search_fields = ['username', 'email']
	list_filter = ['campaign_data__country', PlanFilter]

	#
	# Other settings
	#
	list_select_related = ('settings', 'campaign_data')
	ordering = ('-date_joined',)
	change_list_filter_template = "admin/filter_listing.html"



admin.site.register(User, UserAdmin)





