from azure.storage import BlobService
import os, time

# credentials
blob_service = BlobService(account_name='videopathmobilefiles', account_key='Xxfn5At6O7QmFrwz1XZV7vwXoLQhY7lHAg0Wvmo42CgJc6iY54bEUGaqd7ewpfTS7EloaD+XT1nDlarYjBoKxg==')


videoname = "pHRnkfvs"


# perform upload
def upload_file(source, container_name, key):

	print source + " --> " + container_name + ": " + keyname

	fileName, fileExtension = os.path.splitext(source)
	content_type = ''

	if fileExtension == ".mp3":
		content_type = "audio/mpeg"
	elif fileExtension == ".jpg":
		content_type = "image/jpeg"
	elif fileExtension == ".png":
		content_type = "image/png"

	while True:
		try:
			blob_service.put_block_blob_from_path(
			    container_name,
			    key,
			    source,
			    x_ms_blob_content_type=content_type,
			    x_ms_blob_cache_control='public, max-age=600'
			)
			break
		except:
			print "retrying..."
			time.sleep(1)


# walk all files in dir and push to bucket


codepath = os.path.dirname(os.path.abspath(__file__)) + "/upload/" + videoname
container_name = videoname.lower()		
blob_service.create_container(container_name, x_ms_blob_public_access='container') 

for path, subdirs, files in os.walk(codepath):
	for name in files:
	    # don't upload hidden files
	    if name[0] == ".":
	        continue

	    pathname = os.path.join(path, name)
	    keyname = pathname.replace(codepath, "")[1:] 

	    upload_file(pathname, container_name, name)

