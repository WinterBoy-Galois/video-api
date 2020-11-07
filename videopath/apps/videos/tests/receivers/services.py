
from videopath.apps.videos.models import Source, Video
from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.videos.services_receiver import jpg_transcode_error, jpg_transcode_success

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()


    def test_jpgs_export_error(self):
    	source = Source.objects.create(
    		service= 'youtube',
    		service_identifier = '092834sdf'
    		)
        v = Video.objects.create(team=self.user.default_team)
        v.draft.source = source
        v.draft.save()

    	jpg_transcode_error({
    		'request': {
                'source': {
                    'key': source.key
                }
            }
    	})


    def test_jpgs_export_success(self):
    	source = Source.objects.create(
    		service= 'youtube',
    		service_identifier = '092834sdf'
    		)
        v = Video.objects.create(team=self.user.default_team)
        v.draft.source = source
        v.draft.save()

    	jpg_transcode_success({'result':
                {
    		"results":{
    			"frames":24
    		},
    		"key":source.key
    	}})
    	source = Source.objects.get(key=source.key)
    	self.assertEqual(source.sprite_support, True)
    	self.assertEqual(source.sprite_length, 24)



