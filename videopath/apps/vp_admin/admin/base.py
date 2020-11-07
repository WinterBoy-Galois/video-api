from django.contrib import admin

#
# Helper for certain things
#
SUPER_USERS = ['david', 'anna']
def is_super_user(request):
	return request.user.username in SUPER_USERS

#
# Base class for our model admin
#
class VideopathModelAdmin(admin.ModelAdmin):
	
	only_superusers = True
	list_display_links = None

	def check_access(self,request):
		if self.only_superusers:
			return is_super_user(request)
		return True

	#
	# Always disable delete permissions
	#
	def has_delete_permission(self, request, obj=None):
		return False

	def has_module_permission(self, request):
		return self.check_access(request)

	def has_change_permission(self, request, obj = None):
		return self.check_access(request)