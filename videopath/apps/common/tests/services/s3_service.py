from django.conf import settings

from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.common.services import service_provider

# Uses the standard django frame testing client
class TestClass(BaseTestCase):

    def setup(self):
        self.service = service_provider.get_service("s3")
        self.assertIsNotNone(self.service)

    def test_upload_and_delete(self):
        key = "some key"
        bucket = settings.AWS_UPLOAD_BUCKET
       	self.service.upload("some random string", bucket, key)
       	self.assertTrue(self.service.check_existence(bucket, key))
       	self.service.delete(bucket,key)
       	
