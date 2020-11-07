from boto import elastictranscoder
from boto import sns

from django.conf import settings

import os
AWS_REGION = os.environ.get('AWS_DEFAULT_REGION','us-west-2')

#
# Start a transcoding job
#
def start_transcoding_job(input, other, outputs):
	transcoder = elastictranscoder.connect_to_region(AWS_REGION)
	job = transcoder.create_job(settings.AWS_PIPELINE_ID, input, other, outputs)

	if job:
		return job['Job']['Id']
	else:
		return False


#
# Confirm SNS subscription
#
def confirm_subscription_topic(topic, token):
	conn = sns.connect_to_region(AWS_REGION)
	return conn.confirm_subscription(topic, token)

#
#
#
def check_connection():
	try:
		# connect
		t = elastictranscoder.connect_to_region(AWS_REGION)

		# check the presets we have defined in the settings
		t.read_pipeline(settings.AWS_PIPELINE_ID)
		# check the pipline we have defined
		t.read_preset(settings.AWS_TRANSCODE_PRESET_ID)
		t.read_preset(settings.AWS_TRANSCODE_PRESET_ID2)
		return True
	except Exception as e:
		return str(e)
