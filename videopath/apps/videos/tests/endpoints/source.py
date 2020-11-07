from videopath.apps.common.test_utils import BaseTestCase

from videopath.apps.videos.models import Video, Source

IMPORT_URL = '/v1/video/{0}/import_source/'
JPG_URL = '/v1/video-revision/{0}/source/jpg_sequence/'

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def test_youtube_import(self):

        # create user and video
        self.setup_users_and_clients()
        v=Video.objects.create(team=self.user.default_team)

        response = self.client_user1.post(IMPORT_URL.format(v.pk), {'url':'https://www.youtube.com/watch?v=PPN3KTtrnZM'})
        self.assertEqual(response.status_code, 200)

        v = Video.objects.get(pk=v.id)
        self.assertEqual(v.draft.source.service, "youtube")

    def test_vimeo_import(self):
        # create user and video
        self.setup_users_and_clients()
        v=Video.objects.create(team=self.user.default_team)

        response = self.client_user1.post(IMPORT_URL.format(v.pk), {'url':'https://vimeo.com/36579366'})
        self.assertEqual(response.status_code, 200)

        v = Video.objects.get(pk=v.id)
        self.assertEqual(v.draft.source.service, "vimeo")

    def test_wistia_import(self):
        # create user and video
        self.setup_users_and_clients()
        v=Video.objects.create(team=self.user.default_team)

        response = self.client_user1.post(IMPORT_URL.format(v.pk), {'url':'http://home.wistia.com/medias/1gaiqzxu03'})
        self.assertEqual(response.status_code, 200)

        v = Video.objects.get(pk=v.id)
        self.assertEqual(v.draft.source.service, "wistia")

    def test_brightcove_import(self):
        # create user and video
        self.setup_users_and_clients()
        v=Video.objects.create(team=self.user.default_team)

        #response = self.client_user1.post(IMPORT_URL.format(v.pk), {'url':'http://players.brightcove.net/4328472451001/default_default/index.html?videoId=4332059708001'})
        #self.assertEqual(response.status_code, 200)
        v = Video.objects.get(pk=v.id)

        # disable brightcove import for now

    def test_custom_import(self):
        self.setup_users_and_clients()
        v=Video.objects.create(team=self.user.default_team)
        data = {
            "mp4":"http://videos.videopath.com/m35T1YU0KHQ8ZEr28fKgM4sS0zfEOQW3.mp4",
            "webm": "http://videos.videopath.com/m35T1YU0KHQ8ZEr28fKgM4sS0zfEOQW3.webm",
            "width":"320",
            "height":"240",
            "duration":"200"
          }
        response = self.client_user1.post(IMPORT_URL.format(v.pk), data)
        self.assertEqual(response.status_code, 200)

        v = Video.objects.get(pk=v.id)
        self.assertEqual(v.draft.source.service, "custom")

    def test_jpg_transcoding(self):
        self.setup_users_and_clients()
        v=Video.objects.create(team=self.user.default_team)
        

        # should not work without source
        response = self.client_user1.put(JPG_URL.format(v.draft.pk))
        self.assertEqual(response.status_code, 404)

        # should work
        s = Source.objects.create(service=Source.SERVICE_YOUTUBE, duration=400)
        v.draft.source = s
        v.draft.save()

        response = self.client_user1.put(JPG_URL.format(v.draft.pk))
        self.assertEqual(response.status_code, 201)

        # access check
        response = self.client_user2.put(JPG_URL.format(v.draft.pk))
        self.assertEqual(response.status_code, 404)

        # wrong service
        s.service=Source.SERVICE_WISTIA
        s.save() 
        response = self.client_user1.put(JPG_URL.format(v.draft.pk))
        self.assertEqual(response.status_code, 400)

        # already transcoded
        s.service=Source.SERVICE_YOUTUBE
        s.sprite_support = True
        s.save()
        response = self.client_user1.put(JPG_URL.format(v.draft.pk))
        self.assertEqual(response.status_code, 400)

        # too long
        s.sprite_support = False
        s.duration=10000
        s.save()
        response = self.client_user1.put(JPG_URL.format(v.draft.pk))
        self.assertEqual(response.status_code, 400)