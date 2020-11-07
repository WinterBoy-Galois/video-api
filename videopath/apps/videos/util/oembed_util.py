import re

from videopath.apps.videos.models import Video
from videopath.apps.files.util import thumbnails_util

# conf
embed_template = '<iframe frameborder="0" allow="autoplay" allowfullscreen="" onmousewheel="event.preventDefault()" width="{0}" height="{1}" src="//player.videopath.com/{2}"></iframe>'
url_regex = "player\.videopath\.com\/([a-zA-Z0-9]{2,20})"

def parse(conf):

	try:
		url = conf.get('url', '')
		maxwidth = int(conf.get('maxwidth', 1024))
		maxheight = int(conf.get('maxheight', 576))
	except:
		return 404

	# extract video id
	m = re.search(url_regex, url)
	if m and len(m.groups()) == 1:
		video_key = m.group(1)
	else: 
		return 404

	# try to load video
	try:
		video = Video.objects.get(key=video_key)
	except Video.DoesNotExist:
		return 404

	if video.published == 0:
		return 401

	# try to load current revision
	try:
		revision = video.current_revision
	except:
		return 401

	# get aspect of current source
	aspect = 1.666

	try:
		source = video.video_sources.latest('created')
		aspect = source.video_aspect
	except:
		aspect = 1.7777

	# get thumbnail url
	thumbnail_url = thumbnails_util.thumbnails_for_revision(revision)['large']

	# calculate width & height
	width = maxwidth
	height = maxwidth / aspect

	if height > maxheight:
		width = width * ( maxheight / height )
		height = maxheight

	width = int(width)
	height = int(height)

	# build template
	html = embed_template.format(width, height, video_key)

	# other metadata
	title = revision.title
	description = revision.description

	result = {
        'version': '1.0',
        'type': 'rich',
        'provider_name': 'Videopath',
        'provider_url': 'https://videopath.com',
        'provider_media_id': video_key,
        'width': width,
        'height': height,
        'aspect': aspect,
        'html': html,
        'title': title,
        'description': description,
        'thumbnail_url': thumbnail_url
    }

	return result
