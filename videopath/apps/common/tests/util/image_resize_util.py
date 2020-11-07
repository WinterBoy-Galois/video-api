import os

from PIL import Image

from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.common.util import image_resize_util

# Uses the standard django frame testing client
class TestClass(BaseTestCase):

	def get_image_path(self, name):
		return os.path.dirname(os.path.abspath(__file__)) + "/" + name


	def test_resize_util_success(self):

		cat_image = self.get_image_path("cat.jpg")
		image_resize_util.resize_image_file_path(cat_image, {})

	def test_resize_util_failure(self):
		cat_image = self.get_image_path("image_resize_util.py")

		failed = False
		try:
			image_resize_util.resize_image_file_path(cat_image, {})
		except:
			failed = True
		self.assertTrue(failed)
	   	
	def test_resize_util_fit(self):
		cat_image = self.get_image_path("cat.jpg")
		result = image_resize_util.resize_image_file_path(cat_image, {
			"operation":"fit",
			"size":(52,52)
			})

		image = Image.open(result)
		width, height = image.size

		self.assertEqual(width, 52)
		self.assertTrue(height, 52)


