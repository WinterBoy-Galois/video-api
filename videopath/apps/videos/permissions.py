import json

from rest_framework import permissions

from videopath.apps.videos.models import VideoRevision, Marker

class AuthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

class VideoRevisionPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET": return True
        if request.method == "POST": return False # revisions can not be created by users
        if request.method == "DELETE": return False # revisions can not be deleted by users
        try:
            data = json.loads(request.body)
            revision = VideoRevision.objects.get(pk=data["id"])
            return revision.has_user_access(request.user, False)
        except Exception:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.has_user_access(request.user, request.method=="GET")


class MarkerPermissions(permissions.BasePermission):

    # only allow access if the video revision belongs to a users video
    def has_permission(self, request, view):
        if request.method in ["GET", "DELETE"]:
            return True
        try:
            data = json.loads(request.body)
            revision = VideoRevision.objects.get(pk=data["video_revision"])
            return revision.has_user_access(request.user, False)
        except Exception:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.has_user_access(request.user, request.method=="GET")

class VideoPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.has_user_access(request.user) and not obj.archived

class MarkerContentPermissions(permissions.BasePermission):

    # make sure the marker content belongs to a video we have access to
    def has_permission(self, request, view):
        if request.method in ["GET", "DELETE"]: return True
        try:
            data = json.loads(request.body)
            marker = Marker.objects.get(pk=data["marker"])

            # disallow creation of multiple content blocks if there already is one fullscreen block present
            if request.method == "POST" and marker.contents.filter(type__in=['website','social']).count() > 0:
                return False

            return marker.has_user_access(request.user, False)
        except Exception:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.has_user_access(request.user, request.method=="GET")
