from django.core.management.base import BaseCommand

from videopath.apps.videos.util import video_export_util
from videopath.apps.videos.models import VideoRevision

class Command(BaseCommand):
    def handle(self, *args, **options):

    	for r in VideoRevision.objects.all():
    		if r.video.team.owner.username == 'babbel':
    			print 'skip'
    		else:
    			r.ui_enable_mobile_portrait = True
    			r.save();

        video_export_util.export_all_videos(verbose=True)
