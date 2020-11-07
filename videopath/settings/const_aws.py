import os

#
# Transcoding pipeline
#
AWS_PIPELINE_ID = os.environ.get("AWS_PIPELINE_ID")
AWS_TRANSCODE_PRESET_ID = '1584652286523-p3unoj'
AWS_TRANSCODE_PRESET_ID2 = '1584652320922-uywayf'

#
# uploads bucket
#
AWS_UPLOAD_BUCKET = 'vp-video-in'

#
# logs bucket
#
AWS_LOGS_BUCKET = 'logs.videopath.com'

#
# video & thumbnails buckets
#
AWS_VIDEOS_BUCKET = 'videos.videopath.com'
AWS_THUMBNAIL_BUCKET = 'thumbs.videopath.com'
AWS_VIDEO_BACKUP_BUCKET = "video-backup.videopath.com"

#
# images buckets
#
AWS_IMAGE_OUT_BUCKET = 'vp-images-prod'
AWS_IMAGE_ICON_FOLDER = 'icon'
AWS_IMAGE_THUMBNAIL_FOLDER = 'thumbnail'

#
# docs bucket and prefixes
#
AWS_DOCS_BUCKET = 'vp-docs'
AWS_DOCS_INVOICE_PREFIX = "invoices/"

#
# Player bucket
#
AWS_PLAYER_BUCKET = 'player-prod.videopath.com'

#
# Dumps bucket
#
AWS_DB_DUMPS_BUCKET = "dumps.videopath.com"

PGBACKUPS_URL = os.environ.get("PGBACKUPS_URL")


#
# Cloudfront IDs
#
AWS_PLAYER_DISTRIBUTION_ID = "EMLA4OYCLIFCC"

