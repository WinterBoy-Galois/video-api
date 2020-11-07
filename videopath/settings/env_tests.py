#
# Some optimizations for the tests
#
DATABASES['default'] = {
	'ENGINE': 'django.db.backends.sqlite3',
	'NAME': ':memory:',
}

#
# Nose
#
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
NOSE_ARGS = [
	'--nocapture',
    # '--with-coverage',
    # '--cover-package=videos',
]

#
# override throttle settings for testing
#
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
        'anon': '100/second'
}

#
# Load mock services
#
SERVICE_MOCKS = True


#
# Workaround to disable migrations in Django 1.7
# https://gist.github.com/NotSqrt/5f3c76cd15e40ef62d09
#
class DisableMigrations(object):
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return "notmigrations"
MIGRATION_MODULES = DisableMigrations()