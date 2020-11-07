
# 
# Upload a file or a string to s3
#
def upload(source, bucket, key, content_type = None, cache_control = None, verify = False, public = False):
	return True

#
# Delete a key
#
def delete(bucket, key):
	return True

#
# List all keys in a bucket
#
def list_keys(bucket, prefix = ""):
	return []

#
# Check existence of a key
#
def check_existence(bucket, key):
	return True

#
# Test access to s3
#
def check_access():
	return True

#
# Check if we have full access to a certain bucket
#
def check_access_to_bucket(bucket):
	return True