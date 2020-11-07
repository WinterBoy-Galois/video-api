import json

from django.shortcuts import get_object_or_404

from videopath.apps.videos.models import Video
from videopath.apps.users.models import Team
from .models import Integration

def authenticate_service_view(service):

	def decorator(view):
		def _wrapped_view(request, team_id=None, *args, **kwargs):
			t = Team.objects.teams_for_user(request.user).distinct().get(pk = team_id)
			s = get_object_or_404(Integration, team=t, service=service)
			return view(request, json.loads(s.credentials), *args, **kwargs)
		return _wrapped_view

	return decorator

def authenticate_service_viewset(service):

	def decorator(view):
		def _wrapped_view(instance, request, team_id=None, *args, **kwargs):
			t = Team.objects.teams_for_user(request.user).distinct().get(pk = team_id)
			s = get_object_or_404(Integration, team=t, service=service)
			return view(instance, request, json.loads(s.credentials), *args, **kwargs)
		return _wrapped_view

	return decorator


def authenticate_service_beacon(service):

	def decorator(view):
		def _wrapped_view(request, *args, **kwargs):
			video_key = request.GET.get('video_key', '')
			v = get_object_or_404(Video, key=video_key)
			s = get_object_or_404(Integration, team=v.team, service=service)
			return view(request, json.loads(s.credentials), v.team.owner, *args, **kwargs)
		return _wrapped_view

	return decorator