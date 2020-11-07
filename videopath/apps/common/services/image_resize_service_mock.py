from videopath.apps.files.models import ImageFile

def resize_image_file(f):

    # success
    f.status = ImageFile.PROCESSED
    f.save()