from django.core.management.base import BaseCommand

from videopath.apps.videos.util import video_export_util

class Command(BaseCommand):
    def handle(self, *args, **options):
        video_export_util.export_all_videos(verbose=True)
