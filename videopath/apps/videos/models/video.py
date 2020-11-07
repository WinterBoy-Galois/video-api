import copy, datetime

from django.db import models
from videopath.apps.users.models import Team
from django.conf import settings

from videopath.apps.common.models import VideopathBaseModel

from django.http import Http404

class Videos(models.Manager):

    #
    # Get video for user and perform access check
    #
    def get_video_for_user(self, user, pk=None, key=None):

        if pk:
            try: 
                return self.filter_for_user(user).distinct().get(pk=pk, archived=False)
            except self.model.DoesNotExist: pass

        if key:
            try:
                return  self.filter_for_user(user).distinct().get(key=key, archived=False)
            except self.model.DoesNotExist: pass

        raise Http404


    def filter_for_user(self,user):
        return self.filter( models.Q(team__owner = user) | models.Q(team__members = user) )


class Video(VideopathBaseModel):

    # custom manager class
    objects = Videos()

    # constants
    PRIVATE = 0
    PUBLIC = 1
    PUBLISH_CHOICES = (
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    )
    PLAYER_VERSION_CHOICES = (
        ("1", "1 - Scruffy"),
        ("2", "2 - Bender"),
        ("3", "3 - Zoidberg"),
        ("4", "4 - Zap Brannigan"),
        ("5", "5 - Leila"),
        ("6", "6 - Hedonism Bot")
    )

    # owner
    team = models.ForeignKey(Team, related_name='videos')

    # public stuff
    key = models.CharField(
        max_length=50, blank=True, unique=True, db_index=True)
    published = models.IntegerField(default=PRIVATE, choices=PUBLISH_CHOICES)

    # revisions
    draft = models.OneToOneField(
        "VideoRevision", related_name="video_draft", blank=True, null=True, on_delete=models.SET_NULL)
    current_revision = models.OneToOneField(
        "VideoRevision", related_name="video_current", blank=True, null=True, on_delete=models.SET_NULL)

    # analytics
    total_plays = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)

    # code version
    player_version = models.CharField(
        max_length=20, choices=PLAYER_VERSION_CHOICES, default=settings.PLAYER_DEFAULT_VERSION)

    # define wether video is archived
    archived = models.BooleanField(default=False)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "key__icontains",)

    def has_user_access(self, user):
        return ( self.team.owner == user ) or (self.team.members.filter(username=user.username).count() > 0)


    def duplicate(self):

        # create a copy of the draft
        duplicate = copy.copy(self)

        duplicate.pk = None
        duplicate.key = None

        # make sure we only have one revision as draft
        # and the video is marked as unpublished
        duplicate.draft = self.draft.duplicate()
        duplicate.current_revision = None
        duplicate.published = 0

        # clean up some other values
        duplicate.total_plays = 0
        duplicate.total_views = 0
        duplicate.archived = False

        duplicate.save()

        duplicate.draft.video = duplicate
        duplicate.draft.save()

        return duplicate

    #
    # Can be removed again after migration
    #
    def ensure_draft(self):
        if self.draft_id == None:
            if self.current_revision_id != None:
                self.draft = self.current_revision.duplicate()
                self.save()


    def get_current_revision_or_draft(self):
        if self.current_revision_id != None:
            return self.current_revision
        else:
            return self.draft  

    # publish / unpublish
    def publish(self):
        if self.draft == None:
            return

        self.current_revision = self.draft.duplicate()
        self.current_revision.published_date = datetime.datetime.now()
        self.current_revision.save()

        self.published = 1
        self.save()

        from videopath.apps.videos.util import video_export_util
        video_export_util.export_video(self)

    def unpublish(self):
        if self.current_revision == None:
            pass
        else:
            self.current_revision = None
        self.published = 0
        self.save()
        from videopath.apps.videos.util import video_export_util
        video_export_util.delete_export(self)

    def reexport(self):
        if not self.published:
            return
        from videopath.apps.videos.util import video_export_util
        video_export_util.export_video(self)

    def enable_mobile_portrait(self):
        for r in self.revisions.all():
            r.ui_enable_mobile_portrait = True
            r.save()
        self.reexport()

    def export_jpg_sequence(self):
        if self.draft.source:
            return self.draft.source.export_jpg_sequence()
        return False

    # generate key on save
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(8)
        super(Video, self).save(*args, **kwargs)

    # name
    def __unicode__(self):
        return u'%s %s' % (self.key, self.team)

    # met stuff
    class Meta:
        app_label = "videos"

