from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.videos.models import Video, Marker, MarkerContent

# Uses the standard django frame testing client
class EndpointsBaseTestCase(BaseTestCase):
        
    def setup_users_clients_and_videos(self):
        self.setup_users_and_clients()

        self.video = Video.objects.create(team=self.user1.default_team)

        self.markers = [
            Marker.objects.create(video_revision=self.video.draft),
            Marker.objects.create(video_revision=self.video.draft),
        ]

        self.contents = [
            MarkerContent.objects.create(marker=self.markers[0]),
            MarkerContent.objects.create(marker=self.markers[0]),
            MarkerContent.objects.create(marker=self.markers[0]),
            MarkerContent.objects.create(marker=self.markers[1]),
        ]