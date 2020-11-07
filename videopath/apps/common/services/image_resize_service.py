from boto.s3.connection import S3Connection
from PIL import Image

from django.conf import settings

from videopath.apps.files.settings import image_sizes
from videopath.apps.files.models import ImageFile

_filename_in = "/tmp/image_resize_in"
_filename_out = "/tmp/image_resize_out"

def resize_image_file(f):

    # only process fresh files
    if f.status != ImageFile.FILE_RECEIVED:
        return 

    # try actual processing
    try:
        _resize_image_file(f)
    except Exception as e:
        f.status = ImageFile.ERROR
        f.save()
        return

    # success
    f.status = ImageFile.PROCESSED
    f.save()


def _resize_image_file(f):    

    # s3 connetion
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    in_bucket = conn.get_bucket(settings.AWS_UPLOAD_BUCKET)
    out_bucket = conn.get_bucket(settings.AWS_IMAGE_OUT_BUCKET)

    # conf for image type
    conf = image_sizes[f.image_type]

    # try to retrieve image file
    in_key = in_bucket.get_key(f.key)
    if in_key is None or in_key.size > 5000000:
        f.status == ImageFile.ERROR
        f.save()
        return

    in_key.get_contents_to_filename(_filename_in)

    for out in conf["outs"]:

        # convert image
        has_transparency = False
        image = Image.open(_filename_in)
        if image.mode == "RGBA" or image.mode == "transparency":
            has_transparency = True
        image = image.convert("RGBA")

        image.thumbnail((out["maxWidth"], out["maxHeight"]), Image.ANTIALIAS)

        image.save(_filename_out, "PNG" if has_transparency else "JPEG", quality=90)

        # save image back to s3
        key = out["key"].replace("_FILEKEY_", f.key)
        out_key = out_bucket.new_key(key)
        out_key.set_contents_from_filename(_filename_out, policy="public-read")

        # update file object
        width, height = image.size
        f.width = width
        f.height = height
        f.save()
