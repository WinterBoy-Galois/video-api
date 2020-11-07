import os
import gzip
import StringIO

from boto.s3.connection import S3Connection

from django.conf import settings

connection = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, is_secure=False)

# 
# Upload a file or a string to s3
#
def upload(source, bucket, key, content_type = None, cache_control = None, verify = False, public = False):
	
	# get key
	bucket = connection.get_bucket(bucket)
	key = bucket.new_key(key)

	# set metadata
	if content_type:
		key.set_metadata("Content-Type", content_type)
	if cache_control:
		key.set_metadata("Cache-Control", cache_control)

	# define access policy
	policy = "public-read" if public else "private"

	# define wether to upload from file or from string
	if isinstance(source, basestring):

		# upload from file path
		# read file into string
		if os.path.exists(source):
			with open (source, "r") as myfile:
				source=myfile.read()

		try:
			source = source.encode('utf8')
		except:
			pass

		# gzip string
		out = StringIO.StringIO()
		with gzip.GzipFile(fileobj=out, mode="w") as f:
  			f.write(source)
  		source = out.getvalue()

		# upload from string
		key.set_metadata("Content-Encoding", "gzip")
		key.set_contents_from_string(source, policy=policy)
	else:
		pass

	if verify:
		# verify upload
		pass

	return True

#
# Delete a key
#
def delete(bucket, key):
    bucket = connection.get_bucket(bucket)
    bucket.delete_key(key)
    return True

#
# List all keys in a bucket
#
def list_keys(bucket, prefix = ""):
	bucket = connection.get_bucket(bucket)
	return bucket.list(prefix=prefix)

#
# Check existence of a key
#
def check_existence(bucket, key):
	bucket = connection.get_bucket(settings.AWS_UPLOAD_BUCKET)
	key = bucket.get_key(key)
	return key != None

#
#
#
def check_access():
	try:
		connection.get_all_buckets()
		return True
	except Exception as e:
		return str(e)

#
# Check if we have full access to a certain bucket
#
def check_access_to_bucket(bucket):
	try:
		upload("test", bucket, "test_key")
		delete(bucket, "test_key")
		return True
	except Exception as e:
		return str(e)