from django.contrib.auth.decorators import user_passes_test

def group_membership_required(group, login_url='admin:login'):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
    	if user:
    		for g in user.groups.all():
    			print g
        	return user.groups.filter(name=group).count() > 0
        return False
        # As the last resort, show the login form
    return user_passes_test(check_perms, login_url=login_url)