#! ../venv/bin/python

import os, math
from PIL import Image


skipconvert = False
num_threads = 10

# conf
output_folder = "output-test/"

# vars
audio_file_name = output_folder + "/audio.mp3"
image_file_name = output_folder + "/image_%05d.jpg"
sprite_file_name = output_folder + "/sprite_{0}.jpg"
filename = 'input.mp4'

# extract audio
print "=== Converting Audio ==="
command = "ffmpeg -i {0} -b:a 192k -map a {1}".format(filename, audio_file_name) 
os.system(command)

print "=== Converting Images ==="
command = "ffmpeg -i {0} -r 25 -vf scale=320:180 -q:v 1 -an -f image2 {1}".format(filename, image_file_name) 
os.system(command)


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

	sprite.save(sprite_file_name.format(str(sprite_index).zfill(5)), 'JPEG', quality=50)
