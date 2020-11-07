from django.conf import settings

from videopath.apps.common.services import service_provider

logger = settings.LOGGER

s3_service = service_provider.get_service("s3")
elastic_transcoder_service = service_provider.get_service("elastic_transcoder")

#
# Handle uploads
#
def get_upload_endpoint(expires_in=6000, key=None, method='POST'):
    return "https://" + settings.AWS_UPLOAD_BUCKET + ".s3.amazonaws.com"

def verify_upload(ticket_id=None):
    return s3_service.check_existence(settings.AWS_UPLOAD_BUCKET, ticket_id)

def start_transcoding_video(video):
    logger.info('start_transcoding_video')

    t_input = {
        'Key': video.key,
        'FrameRate': 'auto',
        'Resolution': 'auto',
        'AspectRatio': 'auto',
        'Interlaced': 'auto',
        'Container': 'auto',
    }

    composition = [{
        'TimeSpan': {
            'StartTime': '00000.000',
            'Duration': '01200.000',  # 20 minutes limit on clips
        }
    }]

    t_output_mp4 = {
        'Key': video.key + '.mp4',
        'ThumbnailPattern': video.key + '/{count}-hd',
        'Rotate': 'auto',
        'PresetId': settings.AWS_TRANSCODE_PRESET_ID,
        'Composition': composition,
    }

    t_ouput_webm = {
        'Key': video.key + '.webm',
        'ThumbnailPattern': video.key + '/{count}',
        'Rotate': 'auto',
        'PresetId': settings.AWS_TRANSCODE_PRESET_ID2,
        'Composition': composition,
    }

    return elastic_transcoder_service.start_transcoding_job(t_input, None, [t_output_mp4, t_ouput_webm])


def delete_video_files_for_key(file_key):

    # delete file from in bucket
    s3_service.delete(settings.AWS_UPLOAD_BUCKET, file_key)

    # delete from out bucket
    for key in s3_service.list_keys(settings.AWS_VIDEOS_BUCKET, prefix = file_key):
        s3_service.delete(settings.AWS_VIDEOS_BUCKET, key)

    # delete from thumbs bucket
    for key in s3_service.list_keys(settings.AWS_THUMBNAIL_BUCKET, prefix = file_key):
        s3_service.delete(settings.AWS_THUMBNAIL_BUCKET, key)


def delete_image_files_for_key(file_key):
    s3_service.delete(settings.AWS_UPLOAD_BUCKET, file_key)
    s3_service.delete(settings.AWS_IMAGE_OUT_BUCKET, file_key)


def confirm_subscription(topic, token):
    return elastic_transcoder_service.confirm_subscription_topic(topic, token)

