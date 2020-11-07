
import humanize

from django.contrib import admin

from videopath.apps.videos.models import Video, Marker, MarkerContent, VideoRevision, PlayerAppearance, Source

from videopath.apps.videos.util import video_export_util

#
# Video
#
class VideoAdmin(admin.ModelAdmin):

    # fields
    list_display = ('key', 'id', 'team', 'revision_link', 'created_humanized',
                    'modified_humanized',  'draft_link', 'current_revision_link', 'archived', 'player_version')
    ordering = ('-created',)
    search_fields = ['key', 'id', 'team__owner__username', 'team__owner__email']
    exclude = ['draft','current_revision']

    raw_id_fields = ['team',]
    autocomplete_lookup_fields = {
        'fk': ['team',],
    }

    # actions
    actions=["make_published", "make_unpublished", "make_duplicated", "make_reexport", "make_export_jpgs", "make_mobile_portrait"]
    def make_published(self, request, queryset):
        for video in queryset.all():
            video.publish()

    make_published.short_description = "Publish selected videos"

    def make_unpublished(self, request, queryset):
        for video in queryset.all():
            video.unpublish()
    make_unpublished.short_description = "Unpublish selected videos"

    def make_duplicated(self, request, queryset):
        for video in queryset.all():
            copy = video.duplicate()
            self.message_user(request, "Duplicated video " + video.key + " -> " + copy.key)
    make_duplicated.short_description = "Duplicate selected videos"

    def make_reexport(self, request, queryset):
        for video in queryset.all():
            video_export_util.export_video(video)
    make_reexport.short_description = "Reexport selected videos"

    def make_export_jpgs(self, request,queryset):
        for video in queryset.all():
            video.export_jpg_sequence()
    make_export_jpgs.short_description = "Export JPGs"

    def make_mobile_portrait(self, request, queryset):
        for video in queryset.all():
            video.enable_mobile_portrait()
    make_mobile_portrait.short_description = "Enable for mobile portrait"

    # custom fields
    def created_humanized(self, obj):
        return humanize.naturaltime(obj.created)

    def modified_humanized(self, obj):
        return humanize.naturaltime(obj.modified)

    def revision_link(self, obj):
        link = "/admin/videos/videorevision/?video__key=" + obj.key
        return "<a href = '" + link + "'>List of Revisions</a> (" + str(obj.revisions.count()) + ")"
    revision_link.allow_tags = True

    def draft_link(self, obj):
        if not obj.draft:
            return "None"
        link = "/admin/videos/videorevision/" + str(obj.draft.id)
        return "<a href = '" + link + "'>Current Draft</a>"
    draft_link.allow_tags = True

    def current_revision_link(self, obj):
        if not obj.current_revision:
            return "None"
        link = "/admin/videos/videorevision/" + \
            str(obj.current_revision.id)
        return "<a href = '" + link + "'>Current Revision</a>"
    current_revision_link.allow_tags = True

    def __unicode__(self):
        return "Video " + self.key

admin.site.register(Video, VideoAdmin)


#
# Marker
#
class MarkerInlineAdmin(admin.TabularInline):
    model = Marker

#
# Revision
#
class VideoRevisionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'marker_link', 'created_humanized', 'modified_humanized')
    search_fields = ['title', 'video__key']
    ordering = ('-created',)
    list_filter = ('video__key', 'id')
    inlines = (MarkerInlineAdmin, )

    raw_id_fields = ['video',]
    autocomplete_lookup_fields = {
        'fk': ['video',],
    }

    fieldsets = (
        ('General', {
            'fields': ('video', 'title', 'description', 'published_date')
        }),
        ('Password', {
            'fields': ( 'password', 'password_salt', 'password_hashed' )
        }),
        ('Source', {
            'fields': ('source', )
        }),
        ('Appearance', {
            'fields': ('ui_color_1', 'ui_color_2', 'ui_icon', 'ui_icon_link_target','player_appearance', 'continuous_playback', 'ui_enable_mobile_portrait')
        }),
        ('Endscreen', {
            'fields': ('endscreen_title', 'endscreen_background_color', 'endscreen_button_title', 'endscreen_button_target', 'endscreen_button_color')
        }),

        ('Files', {
            'fields': ('custom_thumbnail', )
        }),

    )

    readonly_fields=('password_hashed', 'password_salt')

    def created_humanized(self, obj):
        return humanize.naturaltime(obj.created)

    def modified_humanized(self, obj):
        return humanize.naturaltime(obj.modified)

    def marker_link(self, obj):
        link = "/admin/videos/marker/?video_revision__id=" + str(obj.id)
        return "<a href = '" + link + "'>List of Markers</a> (" + str(obj.markers.count()) + ")"
    marker_link.allow_tags = True

admin.site.register(VideoRevision, VideoRevisionAdmin)


#
# Marker
#
class MarkerAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'video_revision', 'created', 'content_link')
    list_filter = ('video_revision__id',)
    ordering = ('time',)
    search_fields = ['key', 'id', ]


    def content_link(self, obj):
        link = "/admin/videos/markercontent/?marker__id=" + str(obj.id)
        return "<a href = '" + link + "'>List of Contents</a> (" + str(obj.contents.count()) + ")"
    content_link.allow_tags = True

admin.site.register(Marker, MarkerAdmin)


#
# Marker Content
#
class MarkerContentAdmin(admin.ModelAdmin):
    list_display = ('ordinal', 'type')
    list_filter = ('marker__id',)
    ordering = ('ordinal',)
    search_fields = ['key', 'id', ]

admin.site.register(MarkerContent, MarkerContentAdmin)


#
# Appearance
#
class PlayerAppearanceAdmin(admin.ModelAdmin):

    raw_id_fields = ['user',]
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }

    fieldsets = (
        ('General', {
            'fields': ('description', 'user')
        }),
        ('Colors', {
            'fields': ('ui_color_1', 'ui_color_2')
        }),
        ('Colors Advanced', {
            'fields': (
                ('ui_color_playbar_outline','ui_color_playbar_background','ui_color_playbar_progress','ui_color_playbar_buffer', 'ui_color_playbar_indicators'),
                ('ui_color_marker_background','ui_color_marker_outline','ui_color_marker_text'),
                ('ui_color_marker_highlight_background','ui_color_marker_highlight_outline','ui_color_marker_highlight_text'),
                ('ui_color_button_background','ui_color_button_text','ui_color_button_highlight_background','ui_color_button_highlight_text'),
                ('ui_color_overlay_outline',))
        }),
        ('Images', {
            'fields': ('endscreen_logo', 'ui_icon', 'ui_icon_link_target')
        }),
        ('Fonts', {
            'fields': ('ui_font_marker', 'ui_font_overlay_titles', 'ui_font_overlay_text')
        }),
        ('Other', {
            'fields': ('ui_language','ui_click_hint_appearences','ui_click_hint_color')
        })
    )

admin.site.register(PlayerAppearance, PlayerAppearanceAdmin)

#
# Video Source
#
class SourceAdmin(admin.ModelAdmin):

    list_display = ( 'service', 'key', 'created', 'sprite_support')
    search_fields = ['key', 'revisions__video__key', 'revisions__video__team__owner__username']
    list_filter = ('service', 'sprite_support')

    actions=["make_export_jpgs",]

    def make_export_jpgs(self, request,queryset):
        for source in queryset.all():
            source.export_jpg_sequence()
    make_export_jpgs.short_description = "Export JPGs"

    fieldsets = (
        ('General', {
            'fields': ('key', 'status')
        }),
        ('Service info', {
            'fields': ('service', 'service_identifier')
        }),
        ('Metadata', {
            'fields': ('duration', 'aspect')
        }),
        ('Sources', {
            'fields': ('file_mp4', 'file_webm', 'thumbnail_large', 'thumbnail_small')
        }),
        ('JPG Support', {
            'fields': ('sprite_support', 'sprite_length')
        }),
        ('Other', {
            'fields': ('description','youtube_allow_clickthrough')
        })
    )

admin.site.register(Source, SourceAdmin)

