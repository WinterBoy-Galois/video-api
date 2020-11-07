import copy

from django.db import models
from videopath.apps.users.models import User

from videopath.apps.common.models import VideopathBaseModel, ColorField

class PlayerAppearance(VideopathBaseModel):

    # constants
    LANG_EN = "en"
    LANG_DE = "de"
    LANG_FR = "fr"
    LANGUAGE_CHOICES = (
        (LANG_EN, 'English'),
        (LANG_DE, 'German'),
        (LANG_FR, 'French'),
    )

    # info, may not be needed for now
    description = models.CharField(max_length=255, blank=True, null=True)

    # attached to a whole user, as default player appearance
    user = models.OneToOneField(User,
                                blank=True,
                                null=True,
                                unique=True,
                                related_name='default_player_appearance')

    # simple color generation with two colors  
    ui_color_1 = ColorField(blank=True, null=True)
    ui_color_2 = ColorField(blank=True, null=True)


    # playbar
    ui_color_playbar_outline = ColorField(blank=True, null=True)
    ui_color_playbar_background = ColorField(blank=True, null=True)
    ui_color_playbar_progress = ColorField(blank=True, null=True)
    ui_color_playbar_buffer = ColorField(blank=True, null=True)
    ui_color_playbar_indicators = ColorField(blank=True, null=True)

    # marker regular
    ui_color_marker_background = ColorField(blank=True, null=True)
    ui_color_marker_outline = ColorField(blank=True, null=True)
    ui_color_marker_text = ColorField(blank=True, null=True)

    # marker highlighted
    ui_color_marker_highlight_background = ColorField(blank=True, null=True)
    ui_color_marker_highlight_outline = ColorField(blank=True, null=True)
    ui_color_marker_highlight_text = ColorField(blank=True, null=True)

    # buttons
    ui_color_button_background = ColorField(blank=True, null=True)
    ui_color_button_text = ColorField(blank=True, null=True)
    ui_color_button_highlight_background = ColorField(blank=True, null=True)
    ui_color_button_highlight_text = ColorField(blank=True, null=True)

    # overlays
    ui_color_overlay_outline = ColorField(blank=True, null=True)

    # fonts, takes urls to woff files
    ui_font_marker = models.CharField(max_length=255, blank=True, null=True)
    ui_font_overlay_titles = models.CharField(max_length=255, blank=True, null=True)
    ui_font_overlay_text = models.CharField(max_length=255, blank=True, null=True)

    # additional endscreen settings
    endscreen_logo = models.CharField(max_length=255, blank=True, null=True)

    # icon
    ui_icon = models.CharField(max_length=255, blank=True, null=True)
    ui_icon_link_target = models.CharField(max_length=1024, blank=True, null=True)

    #
    ui_click_hint_color = ColorField(default='#ffffff')
    ui_click_hint_appearences = models.IntegerField(default=1)

    # language
    ui_language = models.CharField(max_length=50,choices=LANGUAGE_CHOICES, default=LANG_EN)


    # duplicate the marker content
    def duplicate(self):
        duplicate = copy.copy(self)
        duplicate.pk = None
        duplicate.user = None
        duplicate.video_revision = None
        duplicate.save()
        return duplicate

    # name
    def __unicode__(self):
        return u'%s (%s)' % (self.description, self.user)

    class Meta:
        app_label = "videos"
