
from django.http import Http404

from django.db.models import Q

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.decorators import permission_classes, renderer_classes, parser_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser


from videopath.apps.videos.util.oembed_xml_renderer import OEmbedXMLRenderer
from videopath.apps.videos.util import share_mail_util, oembed_util, icon_util
from videopath.apps.videos.permissions import MarkerPermissions, VideoPermissions, MarkerContentPermissions, VideoRevisionPermissions, AuthenticatedPermission
from videopath.apps.videos.models import Video, Marker, MarkerContent, VideoRevision, Source
from videopath.apps.videos.serializers import VideoRevisionDetailSerializer, VideoSerializer, MarkerSerializer, MarkerContentSerializer, VideoRevisionSerializer
from videopath.apps.common.services import service_provider
from videopath.apps.users.models import Team

from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny


#
# Upload or delete icon
#
@api_view(['DELETE', 'PUT'])
@permission_classes((AllowAny,))
@parser_classes((MultiPartParser,FormParser))
def icon_view(request, rid=None):

    try:
        revision = VideoRevision.objects.filter_for_user(request.user).distinct().get(pk=rid)
        if request.method == "PUT":
            ok, detail = icon_util.handle_uploaded_icon(revision, request.data["file"])
            if not ok:
                raise ValidationError(detail)
            return Response({},201)
        elif request.method == "DELETE":
            revision.ui_icon = None
            revision.save()
    except VideoRevision.DoesNotExist:
        raise Http404

    

#
# Upload or delete thumbnail
#
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes((AllowAny,))
@parser_classes((MultiPartParser,FormParser))
def thumbnail_view(request, rid=None):

    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    elif request.method == "GET":
        pass

    return Response({})

#
# Support for oEmbed info
#
@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,OEmbedXMLRenderer,))
def oembed(request):

    result = oembed_util.parse(request.GET)

    if result == 401:
        return Response(status=401)
    elif result == 404:
        return Response(status=404)

    return Response(result)

#
# Get revision of a video
#
@api_view(['GET'])
def get_revision(request, vid=None, rev_type='published'):

    # see wether this should be the published or draft version
    published = rev_type == 'published'

    # see wether this should be the expanded view
    expanded = request.GET.get('expanded', '0')

    # load the video and the correct serializer
    video = Video.objects.get_video_for_user(request.user, pk = vid)

    # find the correct revision
    if published and video.current_revision_id:
        revision = video.current_revision
    elif not published:
        revision = video.draft
    else:
        raise Http404

    serializer = VideoRevisionDetailSerializer(revision) if expanded else VideoRevisionSerializer(revision)
    return Response(serializer.data)


#
# Publish and unpublish a video
#
@api_view(['PUT', 'DELETE'])
def video_publish(request, vid=None):

    video = Video.objects.get_video_for_user(request.user,pk=vid)

    if request.method == 'PUT':
        video.publish()
        slack = service_provider.get_service("slack")
        slack.notify("User " + request.user.email + " just published video http://player.videopath.com/" + video.key + ". ")

    if request.method == 'DELETE':
        video.unpublish()

    return Response({})

#
# Send a share email
# 
@api_view(['POST'])
def send_share_mail(request, vid=None):
    video = Video.objects.get_video_for_user(request.user,pk=vid)
    success, detail = share_mail_util.send_share_mail(video, request.data.get("recipients", ""), request.data.get("message",""))

    if not success:
        raise ParseError(detail=detail)

    return Response({})

#
# View Set of Videos
#
class VideoViewSet(viewsets.ModelViewSet):

    model = Video
    serializer_class = VideoSerializer
    permission_classes = (VideoPermissions,AuthenticatedPermission)

    # Can see only your videos, filterable by q
    def get_queryset(self,team_id = None):
        
        videos = Video.objects.filter_for_user(self.request.user).filter(archived=False)

        # filter by team
        team_id = self.request.resolver_match.kwargs.get('team_id', None)
        if team_id:
            videos = videos.filter(team_id=team_id)

        # filter by query
        q = self.request.GET.get('q')
        if q:
            q = q.strip()
            videos = videos.filter(Q(draft__title__icontains = q) | Q(draft__description__icontains = q))

        return videos.extra(order_by=['-created']).distinct()

    def perform_update(self, serializer):
        instance = serializer.save()

        revert_revision = self.request.data.get("revert_revision", None)
        if revert_revision:
            try:
                revision = VideoRevision.objects.get(pk = revert_revision, video=instance)
                instance.draft.delete()
                instance.draft = revision.duplicate()
                instance.save()
            except VideoRevision.DoesNotExist:
                pass


    def perform_create(self, serializer):

        # find correct team for video
        team_id = self.request.data.get('team')
        team = self.request.user.default_team
        if team_id:
            try: team = Team.objects.get(pk=team_id)
            except Team.DoesNotExist: pass

        instance = serializer.save(team=team)

        #
        # see if this video should be a copy of an existing one
        #
        copy_source=self.request.data.get("copy_source", None)
        if copy_source:
            revision = None
            try:
                video = Video.objects.filter_for_user(self.request.user).distinct().get(pk=copy_source)
                revision = video.draft
            except Video.DoesNotExist:
                try:
                    revision = VideoRevision.objects.filter_for_user(self.request.user).distinct().get(pk=copy_source)
                except VideoRevision.DoesNotExist:
                    pass

            if revision:
                revision_copy = revision.duplicate()
                revision_copy.video = instance
                revision_copy.save()
                instance.draft.delete()
                instance.draft = revision_copy
                instance.team = revision.video.team
                instance.save()


        # if the demo attribute is present in the request
        # import demo video for this video
        try:
            demo = self.request.data.get("demo_project", None)
            if demo:
                from videopath.apps.videos.models import Source
                thumb = 'https://i.ytimg.com/vi/CovpUAzI6jY/maxresdefault.jpg'
                data = {'service': 'youtube', 'description': 'Videopath Sample Video', 'aspect': 1.7777777777777777, 'thumbnail_small': thumb, 'thumbnail_large': thumb, 'duration': 32.0, 'service_identifier': 'CovpUAzI6jY'}
                instance.draft.source = Source.objects.create( status=Source.STATUS_OK, **data)
                instance.draft.save()
        except:
            raise ValidationError(detail="Unknown demo project")
        

    def destroy(self, request, *args, **kwargs):
        # videos never get deleted, only archived
        obj = self.get_object()
        obj.archived = True
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# Video Revisions View Set
#
class VideoRevisionViewSet(viewsets.ModelViewSet):

    model = VideoRevision
    permission_classes = (VideoRevisionPermissions,AuthenticatedPermission)

    def get_serializer_class(self):
        if self.request.GET.get('expanded', False):
            return VideoRevisionDetailSerializer
        else:
            return VideoRevisionSerializer

    # revisions will always be created through the system
    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # revisions will always be deleted through the system
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Can see only your videos
    def get_queryset(self):
        objects = VideoRevision.objects.filter_for_user(self.request.user)
        vid = self.kwargs.get('vid', None)
        if vid: objects = objects.filter(video__pk=vid)
        return objects.distinct()

#
# Prepare for iphone transcoding
#
@api_view(['PUT'])
def jpg_sequence_view(request, rid=None):
    try:
        revision = VideoRevision.objects.filter_for_user(request.user).distinct().get(pk=rid)
    except VideoRevision.DoesNotExist:
        raise Http404

    if revision.source == None:
        raise Http404

    success, message = revision.source.export_jpg_sequence()
    if not success:
        return Response({"detail": message}, 400)
    return Response({}, 201)



#
# Marker View Set
#
class MarkerViewSet(viewsets.ModelViewSet):
    model = Marker
    serializer_class = MarkerSerializer
    permission_classes = (MarkerPermissions,AuthenticatedPermission)

    def get_queryset(self, vid = None):
  
        vid = self.request.resolver_match.kwargs.get('vid', None)
        objects = Marker.objects.filter_for_user(self.request.user)
        if vid: objects = objects.filter(video_revision__id=vid) 
        return objects.distinct()

#
# Marker Content View Set
#
class MarkerContentViewSet(viewsets.ModelViewSet):
    model = MarkerContent
    serializer_class = MarkerContentSerializer
    permission_classes = (MarkerContentPermissions,AuthenticatedPermission)

    def get_queryset(self, mid = None):
        mid = self.request.resolver_match.kwargs.get('mid', None)
        objects = MarkerContent.objects.filter_for_user(self.request.user)
        if mid: objects = objects.filter(marker__id=mid)
        return objects.distinct()

#
# Import a video from youtube etc.
#
@api_view(['POST', 'GET'])
def import_source(request, key=None):

    # get video
    video = Video.objects.get_video_for_user(request.user, pk=key)

    service = service_provider.get_service("video_source_import")

    try:
        if "url" in request.data:
            source = service.import_video_from_url(request.data["url"])
        else:
            source = service.import_video_from_server(request.data)
    except Exception as e:
        return Response({"error": e.message, "detail": e.message}, 400)

    # create video source objects    
    video.draft.source = Source.objects.create(status=Source.STATUS_OK, **source)
    video.draft.save()

    if "url" in request.data:
        slack = service_provider.get_service("slack")
        slack.notify("User " + request.user.email + " just imported video " + request.data["url"] + ".")

    # hack to enabled yt annotations for babbel. needs to go soon!
    if request.user.username == 'babbel':
        video.draft.source.youtube_allow_clickthrough = True
        video.draft.source.save()

    # try to set title on draft
    try:
        if not video.draft.title or video.draft.title == "New Video":
            video.draft.title = source["description"]
        video.draft.save()
    except:
        pass


    if video.team.owner.can_use_feature('advanced_video_settings'):
        video.export_jpg_sequence()


    return Response()
