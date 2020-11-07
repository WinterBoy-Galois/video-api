from videopath.apps.common.services import service_provider
from videopath.apps.common import mailer

from videopath.apps.videos.models import Source


service = service_provider.get_service("services")

#
# Called when there was an error transcoding a videos to jpgs
#
def jpg_transcode_error(message):
	key = message['request']['source']['key']
	try:
		source = Source.objects.get(key=key)
		for v in source.get_attached_videos():
			mailer.send_mail('jpg_transcode_failed', {'title':v.draft.title}, v.team.owner)
	except Source.DoesNotExist:
		pass 

service.receive_messages('q-transcoder-errors', jpg_transcode_error)

#
# Called when there was a success transcoding videos to jpgs
#
def jpg_transcode_success(message):
	key = message['result']['key']
	try:

		# update source object
		source = Source.objects.get(key=key)

		# only send mails if jpg sequence change is new
		for v in source.get_attached_videos():
			mailer.send_mail('jpg_transcode_succeeded', {'title':v.draft.title}, v.team.owner)

		source.jpg_sequence_support = True
		source.jpg_sequence_length = message['result']['results']['frames']

		source.sprite_support = True
		source.sprite_length = message['result']['results']['frames']

		source.save()

		# reexport all attached video objects
		for v in source.get_attached_videos():
			v.reexport()

		

	except Source.DoesNotExist:
		pass # do nothing..
		
service.receive_messages('q-transcoder-results', jpg_transcode_success)