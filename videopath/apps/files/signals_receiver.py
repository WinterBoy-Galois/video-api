from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.management import call_command
from django.conf import settings

from videopath.apps.files.util.aws_util import delete_image_files_for_key
from videopath.apps.files.models import ImageFile
from videopath.apps.videos.models import MarkerContent
from videopath.apps.vp_admin.signals import daily_jobs


# delete image file object if many to many relationship will be empty
@receiver(pre_delete, sender=MarkerContent)
def delete_image_file_object(sender, instance=None, **kwargs):
    for image_file in instance.image_file.all():
        if image_file.markercontent.count() == 1:
            image_file.delete()

# delete files on s3 if file object is deleted
@receiver(pre_delete, sender=ImageFile)
def delete_all_image_files(sender, instance=None, **kwargs):
    delete_image_files_for_key(instance.key)

# register daily cron jobs
# @receiver(daily_jobs)
# def run_update_video_file_sizes(sender, **kwargs):
#     call_command("update_video_file_sizes")

@receiver(daily_jobs)
def run_backup_videos(sender, **kwargs):
    if settings.STAGING:
        return
    call_command("backup_files")
