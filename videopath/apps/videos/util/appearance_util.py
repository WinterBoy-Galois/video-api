from django.conf import settings

#
# Inject appearance info
#
def appearance_for_revision(revision):

    from videopath.apps.videos.models import PlayerAppearance
    from videopath.apps.videos.serializers import PlayerAppearanceSerializer

   # build appearance in the right order
    result = settings.DEFAULT_VIDEO_APPEARANCE.copy()
    user = revision.video.team.owner

    # merge appearance from model on user 
    try:
        vrs = PlayerAppearanceSerializer(user.default_player_appearance)
        result.update(vrs.data)  
    except PlayerAppearance.DoesNotExist:
        pass

    # merge appearance from model on revision
    try:
        if revision.player_appearance:
            vrs = PlayerAppearanceSerializer(revision.player_appearance)
            result.update(vrs.data)  
    except PlayerAppearance.DoesNotExist:
        pass

    return result