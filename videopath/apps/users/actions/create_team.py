
from videopath.apps.users.models import User, Team

def run(username, teamname):
	user = User.objects.get(username=username)	    
	owner = User.objects.get(pk=1)
	if not user:
		return


	team = Team.objects.create(owner=owner, name=teamname)

	for v in user.default_team.videos.all():
		v.team = team
		v.save()
