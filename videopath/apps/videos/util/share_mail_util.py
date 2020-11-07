import re

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from videopath.apps.files.util.thumbnails_util import thumbnails_for_video

from videopath.apps.common import mailer

def send_share_mail(video, recipients, message):

	recipients = re.split("[\ ,]", recipients)

    # validate emails
	recipients_validated = []
	try:
	    for r in recipients:
	        if len(r.strip()) > 0:
	            validate_email(r)
	            recipients_validated.append({'email':r})
	except ValidationError:
	    return False, "Could not parse recipients"

	if len(recipients_validated) == 0:
	    return False, "No valid recipients"

	mailer.send_mail('share_video', {
		'message': message,
		'description': video.draft.description,
		'title': video.draft.title,
		'link': "http://player.videopath.com/" + video.key, 
		'thumb_url': thumbnails_for_video(video)["large"],
		'to': recipients_validated,
	}, video.team.owner)

	return True, ""
