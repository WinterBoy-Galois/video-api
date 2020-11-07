import os

#
# mandrill
#
MANDRILL_APIKEY = os.environ.get("MANDRILL_APIKEY")

#
# mail chimp
#
MAILCHIMP_APIKEY = os.environ.get("MAILCHIMP_APIKEY")

#
# Stripe
#
STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")

#
# GA access
#
GA_EMAIL = os.environ.get("GA_EMAIL")
GA_PRIVATE_KEY = os.environ.get("GA_PRIVATE_KEY")

#
# AWS
#
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

#
# Raven config
#
RAVEN_CONFIG = {
    'dsn': os.environ.get("RAVEN_KEY"),
}

#
# Slack
#
SLACK_API_TOCKEN = os.environ.get("SLACK_API_TOCKEN")

#
#	Mailchimp Oauth
#
MAILCHIMP_CLIENT_ID = os.environ.get("MAILCHIMP_CLIENT_ID")
MAILCHIMP_CLIENT_SECRET = os.environ.get("MAILCHIMP_CLIENT_SECRET")

VIMEO_CLIENT_ID = os.environ.get("VIMEO_CLIENT_ID")
VIMEO_CLIENT_SECRET = os.environ.get("VIMEO_CLIENT_SECRET")


#
# Pipedrive
#
PIPEDRIVE_API_KEY = os.environ.get("PIPEDRIVE_API_KEY")


#
# Sendgrid
#
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


#
# Youtube 
#
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
