from azure.storage import BlobService
import sys

key = raw_input("Please enter azure vidoepath blob storage key: ")
blob_service = BlobService(account_name='videopathmobilefiles', account_key=key)


source = sys.argv[1]
target = sys.argv[2]


print source + " -> " + target

blob_service.create_container(target, x_ms_blob_public_access='container')

# blob_service.copy_blob('test2', 'copiedkey', '/videopathmobilefiles/test/key')

blobs = blob_service.list_blobs(source)

for b in blobs:
	name = b.name
	source_path = '/videopathmobilefiles/' + source + '/' + name
	blob_service.copy_blob(target, name, source_path)
	print name