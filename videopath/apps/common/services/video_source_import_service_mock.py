

def import_video_from_url( url):

	if "youtube" in url:
		return {
			'service': 'youtube', 
			'description': 'Monty Python - Cheese Shop', 
			'aspect': 1.3333333333333333, 
			'thumbnail_small':'https://i.ytimg.com/vi/PPN3KTtrnZM/hqdefault.jpg', 
			'thumbnail_large':'https://i.ytimg.com/vi/PPN3KTtrnZM/hqdefault.jpg', 
			'duration': 329, 
			'service_identifier': 'PPN3KTtrnZM'
		}

	if "wistia" in url:
		return {
			'service': 'wistia', 
			'description': u'm35T1YU0KHQ8ZEr28fKgM4sS0zfEOQW3', 
			'aspect': 1.6901408450704225, 
			'thumbnail_small': u'https://embed-ssl.wistia.com/deliveries/3c2a7d8c8eae310da1862e3e280704b61ae2b4f7.jpg?image_crop_resized=960x540', 
			'duration': 116.259, 
			'thumbnail_large': u'https://embed-ssl.wistia.com/deliveries/3c2a7d8c8eae310da1862e3e280704b61ae2b4f7.jpg?image_crop_resized=960x540', 
			'service_identifier': '1gaiqzxu03'
		}

	if "vimeo" in url:
		return {
			'service': 'vimeo', 
			'description': 'Bret Victor - Inventing on Principle', 
			'aspect': 1.7777777777777777, 
			'thumbnail_small': 'http://i.vimeocdn.com/video/251172173_640.jpg', 
			'thumbnail_large': 'http://i.vimeocdn.com/video/251172173_640.jpg', 
			'duration': 3260, 
			'service_identifier': '36579366'
		}

	if "brightcove" in url: 
		return {
			'aspect': 1.7777777777777777, 
			'duration': 116.216, 
			'thumbnail_small': u'http://brightcove.vo.llnwd.net/v1/unsecured/media/4328472451001/201507/2799/4328472451001_4332085060001_th-5593bcfde4b0aea8a771006d-672293876001.jpg?pubId=4328472451001&videoId=4332059708001', 
			'thumbnail_large': u'http://brightcove.vo.llnwd.net/v1/unsecured/media/4328472451001/201507/2799/4328472451001_4332085060001_th-5593bcfde4b0aea8a771006d-672293876001.jpg?pubId=4328472451001&videoId=4332059708001', 
			'service': 'brightcove', 
			'service_identifier': {'player': u'33108374-2ef7-4447-b6d3-f0e046e0f70c', 'account': u'4328472451001', 'video_id': u'4332059708001'}
		}

	# moving images
	if "video-cdn" in url:
		return {
			'aspect': 1.7777777777777777,
			'duration': 0,
			'thumbnail_small': '',
			'thumbnail_large': '',
			'service': 'movingimages',
			'service_identifier': {'video_id': u'-BNPey-_eWpKCkw82-UCWt', 'player_id': u'597G7fRQ7Fhe99cC4fEDYp'}
		} 


def import_video_from_server(vars):
	return {
			"service":"custom"
		}