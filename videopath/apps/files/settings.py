from videopath.apps.files.models import ImageFile

# configure different image types
image_sizes = {

    ImageFile.MARKER_CONTENT: {
        "maxSize": 5000000,
        "outs": [{
            "name": "regular",
            "maxWidth": 800,
            "maxHeight": 800,
            "key": "_FILEKEY_"
        }]
    },

    ImageFile.CUSTOM_THUMBNAIL: {
        "outs": [{
            "name": "normal",
            "maxWidth": 384,
            "maxHeight": 216,
            "key": "_FILEKEY_"
        }, {
            "name": "large",
            "maxWidth": 1280,
            "maxHeight": 720,
            "key": "_FILEKEY_-hd"
        }]
    }
}
