import os

STAGING = False
LOCAL = False
CONTINOUS_INTEGRATION = False
PRODUCTION = False

settings_files = [
    # django settings
    "django",
    # aws settings
    "const_aws",
    # api keys, and access
    "const_keys",
    # all our plans
    "plans",
    # list of countries
    "const_countries",
    # vat
    "const_vat_rates",
    # the rest
    "misc"
]

# import all files
for f in settings_files:
    execfile(os.path.join(SITE_ROOT, "settings/" + f + '.py'))

# check if there is a local settings file, load this for development
if os.path.exists(os.path.join(SITE_ROOT, 'settings/env_local.py')):
    execfile(os.path.join(SITE_ROOT, 'settings/env_local.py'))

# Check if we're on the heroku staging server, and load another file for that
if os.environ.get("STAGING") == "TRUE":
    execfile(os.path.join(SITE_ROOT, 'settings/env_staging.py'))

# Check if we're on the heroku production server, and load another file for that
if os.environ.get("PRODUCTION") == "TRUE":
    execfile(os.path.join(SITE_ROOT, 'settings/env_production.py'))

# Check if we're running tests, and load some migrations for them
if 'test' in sys.argv:
    execfile(os.path.join(SITE_ROOT, 'settings/env_tests.py'))

# Check if we're on the continous integration server
if os.environ.get("CI") == "TRUE":
    execfile(os.path.join(SITE_ROOT, 'settings/env_ci.py'))
