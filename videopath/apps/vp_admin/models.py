from videopath.apps.users.models import User as _User
from videopath.apps.videos.models import Video as _Video
from videopath.apps.payments.models import Payment as _Payment

#
# Proxy user model for Sales list
#
class User(_User):
    class Meta:
        proxy = True

#
# Proxy model for videos
#
class Video(_Video):
	class Meta:
		proxy = True

class Payment(_Payment):
	class Meta:
		proxy = True