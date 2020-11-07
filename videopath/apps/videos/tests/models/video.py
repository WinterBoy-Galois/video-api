import datetime

from videopath.apps.videos.models import Video, Source
from videopath.apps.common.test_utils import BaseTestCase

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
        
        # video should be creatable 
        video = Video.objects.create(team=self.user.default_team)
       	self.assertIsNotNone(video)

       	# video should have draft revision
       	self.assertIsNotNone(video.draft)

    def test_publish_unpublish(self):
        video = Video.objects.create(team=self.user.default_team)
        self.assertIsNotNone(video.draft)

      	video.publish()
        self.assertIsNotNone(video.draft)
        self.assertIsNotNone(video.current_revision)
        self.assertNotEqual(video.draft_id, video.current_revision_id)

      	video.unpublish()
        self.assertIsNotNone(video.draft)
        self.assertIsNone(video.current_revision)

        # both revision should still be here
        self.assertEqual(video.revisions.count(), 2)

        #
        # we should now have 3 revisions
        #
        video.publish()
        self.assertEqual(video.revisions.count(), 3)

        video.publish()
        self.assertEqual(video.revisions.count(), 4)


    def test_create_new_draft(self):
        video = Video.objects.create(team=self.user.default_team)
        video.publish()
        self.assertIsNotNone(video.current_revision)
        self.assertIsNotNone(video.draft)

    def test_duplication(self):

        # duplicating video object with file should fail
        video = Video.objects.create(team=self.user.default_team)
        video.draft.source = Source.objects.create()
        video.draft.save()
        duplicate = video.duplicate()
        self.assertIsNotNone(duplicate)


        self.assertEqual(video.revisions.count(), 1)
        self.assertEqual(duplicate.revisions.count(), 1)

        # should be a new copy
        self.assertIsNotNone(duplicate)
        self.assertNotEqual(video.key, duplicate.key)

        # draft should be duplicarted
        self.assertIsNotNone(video.draft)
        self.assertIsNotNone(duplicate.draft)
        self.assertNotEqual(video.draft.pk, duplicate.draft.pk)
        self.assertEqual(video.draft.source.pk, duplicate.draft.source.pk)

        # both share the same source object
        self.assertEqual(Source.objects.count(), 1)

