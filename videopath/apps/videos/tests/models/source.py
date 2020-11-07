
from videopath.apps.videos.models import Source, Video
from videopath.apps.common.test_utils import BaseTestCase

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
        # source should be creatable 
        Source.objects.create()

    def test_jpgs_export(self):
    	source = Source.objects.create(
    		service= 'youtube',
    		service_identifier = '092834sdf'
    		)
    	source.export_jpg_sequence()


    def test_get_attached_vidoes(self):
        v1 = Video.objects.create(team=self.user.default_team)
        v2 = Video.objects.create(team=self.user.default_team)

        s = Source.objects.create()

        v1.draft.source = s
        v1.draft.save()

        v2.draft.source = s
        v2.draft.save()

        s = Source.objects.get(pk=s.pk)

        vids = s.get_attached_videos()

        self.assertEqual(vids.count(),2)



