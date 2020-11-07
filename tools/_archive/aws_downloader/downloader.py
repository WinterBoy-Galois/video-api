from boto.s3.connection import S3Connection
import os


connection = S3Connection("AKIAIG2ODXQTVB5HGGLQ", 'sz5HWoVSN9aG9n4/i+JRa0uUlo+NVez8u2BXaNPI')
bucket = connection.get_bucket("jpgs.videopath.com")

for key in bucket.list("rC60u1Op"):
	filename = os.path.dirname(os.path.abspath(__file__))+"/"+key.name
	dirname = os.path.dirname(filename)
	try:
		os.makedirs(dirname)
	except:
		pass
	try:
		key.get_contents_to_filename(filename)
	except:
		pass

