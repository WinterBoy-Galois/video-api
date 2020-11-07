import copy
from hashlib import sha256

from django.db import models

from videopath.apps.common.models import VideopathBaseModel, ColorField
from videopath.apps.videos.models import Source

class VideoRevisions(models.Manager):

    def filter_for_user(self,user):
        return self.filter( models.Q(video__team__owner = user) | models.Q(video__team__members = user) )


class VideoRevision(VideopathBaseModel):

    objects = VideoRevisions()

    video = models.ForeignKey("videos.Video", related_name="revisions")
    source = models.ForeignKey(
        Source, 
        related_name="revisions",
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL
    )

    title = models.CharField(max_length=255, default="New Video")

    # images (should actually be defined in the files module, works better
    # with a foreign relationship key in this case though)
    custom_thumbnail = models.ForeignKey(
        "files.ImageFile", 
        related_name="video_thumbnail", 
        blank=True, 
        default=None, 
        null=True)

    # model can either be attached to a video revision or
    player_appearance = models.ForeignKey("videos.PlayerAppearance", 
                                            blank=True,
                                            null=True,
                                            default=None,
                                            on_delete=models.SET_NULL,
                                            related_name="video_revisions")

    # meta
    description = models.TextField(blank=True)

    # date when this revision was published (if it was)
    published_date = models.DateTimeField(blank=True, null=True)

    # ui color
    ui_color_1 = ColorField(default="#273a45")
    ui_color_2 = ColorField(default="#ffffff")

    # reference to custom icon if uploaded
    ui_icon = models.CharField(max_length=512, blank=True)
    ui_icon_link_target = models.CharField(max_length=1024, blank=True, null=True, default='https://videopath.com')

    # other ui settings
    ui_disable_share_buttons = models.BooleanField(default=False)
    ui_equal_marker_lengths = models.BooleanField(default=False)
    ui_fit_video = models.BooleanField(default=False)
    ui_enable_mobile_portrait = models.BooleanField(default=True)

    # other settings
    continuous_playback = models.BooleanField(default=False)
    custom_tracking_code = models.CharField(max_length=20, blank=True)
    
    # endscreen settings
    endscreen_title = models.CharField(max_length=512, blank=True)
    endscreen_background_color = ColorField(default="#32526e", blank=True)
    endscreen_button_title = models.CharField(
        default="Try videopath now", max_length=512, blank=True)
    endscreen_button_target = models.CharField(
        default="http://videopath.com", max_length=512, blank=True)
    endscreen_button_color = ColorField(default="#ff6b57", blank=True)
    endscreen_subtitle = models.CharField(
        default="Create your own interactive video", max_length=512, blank=True)

    # password protection
    password = models.CharField(max_length=512, blank=True) # stores the salted sha digest
    password_hashed = models.CharField(max_length=512, blank=True) # helper field for updateing the password
    password_salt = models.CharField(max_length=512, blank=True) # stores the salt specific to this video

    def save(self, *args, **kwargs):
        
        if not self.password_salt:
            self.password_salt = self.generate_key(32)

        # only update hashed password if the value has been changed
        # we detect this by seing if the excerpt of the hash set on the
        # password variable has changed
        if self.password and self.password not in self.password_hashed:
            self.password_hashed = unicode(sha256(self.password+self.password_salt).hexdigest())

        # clear password
        if not self.password:
            self.password_hashed = ""

        # set excerpt of hash on public password variable
        self.password = self.password_hashed[:6]

        super(VideoRevision, self).save(*args, **kwargs)

    def has_user_access(self, user, readonly = True):

        # only allow write access if this is a draft revision
        if not readonly and not self.video_draft:
            return False
        return self.video.has_user_access(user)


    # duplicate the revision
    def duplicate(self):

        # create a copy of the draft
        duplicate = copy.copy(self)
        duplicate.pk = None
        duplicate.save()

        # also dupicate all markers
        for marker in self.markers.all():
            dup_marker = marker.duplicate()
            dup_marker.video_revision = duplicate
            dup_marker.save()

        return duplicate

    def __unicode__(self):
        return "Revision " + str(self.id) + " - " + self.video.key

    class Meta:
        app_label = "videos"

