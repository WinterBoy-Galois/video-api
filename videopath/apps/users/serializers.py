from videopath.apps.users.models import User 
from django.conf import settings

from rest_framework import serializers

from videopath.apps.users.models import UserSettings, Team, TeamMember

#
#
#
class UserSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSettings

#
#
#
class UserSerializer(serializers.ModelSerializer):

    plan = serializers.SerializerMethodField()
    username = serializers.CharField(min_length=3, required=False)

    newsletter = serializers.BooleanField(required=False)

    password = serializers.CharField(min_length=6, required=False, write_only=True)
    new_password = serializers.CharField(min_length=6, required=False)

    def get_plan(self, user):
        plan = "free-free"
        try:
            plan = user.subscription.plan
        except:
            pass
        return settings.PLANS.get(plan, settings.DEFAULT_PLAN)

    class Meta:
        model = User
        fields = ('username', 'default_team', 'email', 'id', 'plan', 'url', 'new_password','password', 'newsletter')
        read_only_fields = ('username', 'id', 'default_team')


class SlimUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')
        read_only_fields = ('username', 'id', 'email')

#
#
#
class TeamSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()
    is_default_team = serializers.SerializerMethodField()

    stats = serializers.SerializerMethodField()

    owner = SlimUserSerializer(read_only=True)

    plan = serializers.SerializerMethodField()

    def get_plan(self, team):
        plan = "free-free"
        try:
            plan = team.owner.subscription.plan
        except:
            pass
        return settings.PLANS.get(plan, settings.DEFAULT_PLAN)

    # todo
    def get_role(self, team):
        user = self.context.get('request').user
        if team.is_user_owner(user): return 'owner'
        if team.is_user_admin(user): return 'admin'
        if team.is_user_member(user): return 'editor'
        return None

    def get_is_default_team(self, team):
        return team.is_a_default_team() 

    def get_stats(self, team):
        return {
            "number_of_videos": team.videos.filter(archived=False).count(),
            "number_of_members": team.members.count()
        }

    class Meta:
        model = Team
        fields = ('owner', 'name', 'id', 'role', 'is_default_team', 'stats', 'created', 'plan')
        read_only_fields = ('owner', 'stats', 'created')


#
#
#
class TeamMemberSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, member):
        return member.user.email

    class Meta:
        model = TeamMember
        fields = ('user', 'team', 'role', 'email', 'created', 'id')
        read_only_fields = ('user', 'team', 'email', 'created')