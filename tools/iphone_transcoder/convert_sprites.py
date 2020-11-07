#! ../venv/bin/python

import os, math
import sys
import shutil
import time

from PIL import Image

from azure.storage.blob import BlobService
from threading import Thread

skipconvert = False
num_threads = 10


# check input
if len(sys.argv) <= 1:
	print "Usage: convert.py <filename.mp4> <video_id>"
	exit()

# input
filename = sys.argv[1]

# conf
output_folder = "output/" + sys.argv[2]

# vars
audio_file_name = output_folder + "/audio.mp3"
image_file_name = output_folder + "/image_%05d.jpg"
sprite_file_name = output_folder + "/sprite_{0}.jpg"

# create folder
if not skipconvert:
	if os.path.exists(output_folder):
		shutil.rmtree(output_folder)
	os.makedirs(output_folder)

	# extract audio
	print "=== Converting Audio ==="
	command = "ffmpeg -i {0} -b:a 192k -map a {1}".format(filename, audio_file_name) 
	os.system(command)

	print "=== Converting Images ==="
	command = "ffmpeg -i {0} -r 25 -vf scale=320:180 -q:v 1 -an -f image2 {1}".format(filename, image_file_name) 
	os.system(command)

print "=== Converting sprites ==="

# convert to sprites
SPRITE_WIDTH = 2
SPRITE_HEIGHT = 17

IMAGE_WIDTH = 320
IMAGE_HEIGHT = 180

# collect files
filepaths = []
basepath = os.path.dirname(os.path.abspath(__file__)) + "/" + output_folder
for path, subdirs, files in os.walk(basepath):
	for name in files:
		# don't upload hidden files
		if 'image' in name:
			pathname = os.path.join(path, name)
			filepaths.append(pathname)

image_count = len(filepaths)
images_in_sprite = SPRITE_WIDTH * SPRITE_HEIGHT
sprite_count = int(math.ceil(float(image_count)/float(images_in_sprite)))

for sprite_index in range(0, sprite_count):

	offset = sprite_index * images_in_sprite
	image_paths = filepaths[offset:offset+images_in_sprite]
	sprite = Image.new("RGB", (IMAGE_WIDTH * SPRITE_WIDTH, IMAGE_HEIGHT * SPRITE_HEIGHT))
	
	print 'processing sprite ' + str(sprite_index)

	count = 0
	for image_path in image_paths:
		offsetX = (count % 2) * IMAGE_WIDTH
		offsetY = ( count / 2 ) * IMAGE_HEIGHT
		frame = Image.open(image_path)
		sprite.paste(frame, (offsetX,offsetY))
		frame.close()
		os.remove(image_path) 
		count+=1

	sprite.save(sprite_file_name.format(str(sprite_index).zfill(5)), 'JPEG', quality=70)

# if there is no video key return
if len(sys.argv) <= 2:
	exit()

print "=== Uploading to Azure ==="

video_key = sys.argv[2]

# walk all files in dir and push to bucket
key = raw_input("Please enter azure vidoepath blob storage key: ")
blob_service = BlobService(account_name='videopathmobilefiles', account_key=key)
basepath = os.path.dirname(os.path.abspath(__file__)) + "/" + output_folder
container_name = video_key.lower()
blob_service.create_container(container_name, x_ms_blob_public_access='container')

# collect files for uploading
filepaths = []
for path, subdirs, files in os.walk(basepath):
	for name in files:
		# don't upload hidden files
		if name[0] == ".":
		    continue
		pathname = os.path.join(path, name)
		filepaths.append(pathname)



# uploading thread
def upload_files(filepaths):
	while len(filepaths):
		pathname = filepaths.pop(0)

		keyname = pathname.replace(basepath, "")[1:]

		print pathname + " --> " + container_name + ": " + keyname

		fileName, fileExtension = os.path.splitext(pathname)
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
				    keyname,
				    pathname,
				    x_ms_blob_content_type=content_type,
				    x_ms_blob_cache_control='public, max-age=600'
				)
				break
			except:
				print "retrying..."
				time.sleep(1)

def sleeper():
		print "thread %d sleeps for 5 seconds" % i
		time.sleep(5)
		print "thread %d woke up" % i

# spawn threads
for i in range(num_threads):
	t = Thread(target=upload_files, args=(filepaths,))
	t.start()
