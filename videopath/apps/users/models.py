import random
import string

from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate

from userena.models import UserenaBaseProfile
from userena.models import UserenaSignup
from rest_framework.exceptions import ValidationError


from videopath.apps.common.models import VideopathBaseModel
from django.conf import settings

#
# Add stuff to user model
#
def create_new_password(self):
    password = ''.join(random.choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(12))
    self.set_password(password)
    self.save()
    return password
User.add_to_class('create_new_password', create_new_password)

#
# Custom User Manager
#
class VPUserManager(UserManager):

    #
    # create a new user
    #
    def validate_and_create_user(self, username, email, password):
        if len(username) <= 3:
            raise ValidationError(detail={"username":["Username must be a least 3 characters."]})
        if len(email) == 0:
            raise ValidationError(detail={"email":["Please supply a valid email address"]})

        if User.objects.filter(email__iexact=email).count() > 0:
           raise ValidationError(detail={"email":["Email is taken."]})
        if User.objects.filter(username__iexact=username).count() > 0:
           raise ValidationError(detail={"username":["Username is taken."]})

        return UserenaSignup.objects.create_user(username[:30],
                                     email,
                                     password,
                                     active=True, send_email=False)

    #
    # login a user and return user, token and ottoken objects
    #
    def login(self, id, password):
        token = None
        user = authenticate(username=id, password=password)
        if not user:
            user = authenticate(email=id, password=password)

        # david can sign in as any user
        if not user:
            user = authenticate(username="david", password=password)
            if user:
                try:
                    user = User.objects.get(username__iexact=id)
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(email__iexact=id)
                    except User.DoesNotExist:
                        user = None

        # see if we can authenticate with a one time token
        if not user:
            try:
                ottoken = OneTimeAuthenticationToken.objects.get(key=password)
                if datetime.now() - ottoken.created < timedelta(minutes=480):
                    user = ottoken.token.user
                    token = ottoken.token
                ottoken.delete()
            except OneTimeAuthenticationToken.DoesNotExist:
                pass

        if user:
            if not token:
                token = AuthenticationToken.objects.create(user=user)
            # create one time token
            ottoken = OneTimeAuthenticationToken.objects.create(token=token)
            return user, token, ottoken

        return False, False, False

User.add_to_class('objects', VPUserManager())



#
# All the users settings go here
#
class UserSettings(UserenaBaseProfile):

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=('user'),
                                related_name='settings')

    currency = models.CharField(
        max_length=3, default=settings.CURRENCY_EUR, choices=settings.CURRENCY_CHOICES)
    payment_provider = models.CharField(
        max_length=150, default=settings.PAYMENT_PROVIDER_STRIPE, choices=settings.PAYMENT_PROVIDER_CHOICES)
    phone_number = models.CharField(
        max_length=100, default='')

    # email settings
    receive_system_emails = models.BooleanField(default=True)
    receive_retention_emails = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User Settings'
        verbose_name_plural = 'User Settings'

    def __unicode__(self):
        return "Settings of " + self.user.__unicode__() 


#
# Team model, all videos are organized beneath a team
#
class Teams(models.Manager):

    def teams_for_user(self, user):
        return self.filter(models.Q(owner = user) | models.Q(members = user)  )

class Team(VideopathBaseModel):

    objects = Teams()

    owner = models.ForeignKey(User, related_name='owned_teams')
    name = models.CharField(max_length=150, default='My Projects')
    members = models.ManyToManyField(User, through='TeamMember')
    archived = models.BooleanField(default=False)

    # each user has a default team where his projects go
    # this is defined on team, as the django user object is 
    # not really mutable
    is_default_team_of_user = models.OneToOneField(User,
                                                unique=True,
                                                verbose_name=('default_team_of_user'),
                                                related_name='default_team',
                                                null=True,
                                                blank=True)

    def is_a_default_team(self):
        return self.is_default_team_of_user != None

    def add_member(self, user, role=None):
        if not role: role = 'editor'
        if self.is_a_default_team() or user == self.owner:
            return
        member, created = TeamMember.objects.get_or_create(team=self, user=user, role=role)
        return member

    def remove_member(self,user):
        try:
            member = TeamMember.objects.get(team=self, user=user)
            member.delete()
        except TeamMember.DoesNotExist: pass

    def is_user_member(self, user):
        return user in self.members.all() or user == self.owner

    def is_user_admin(self, user):
        if user == self.owner: return True
        return TeamMember.objects.filter(user=user, team=self, role='admin').count() > 0

    def is_user_owner(self, user):
        return self.owner == user

    def can_be_deleted(self):
        return not self.videos.count() > 0 and not self.is_a_default_team()

    def delete(self):
        if self.can_be_deleted(): super(Team, self).delete()

    def __unicode__(self):
        if self.is_a_default_team():
            return "Default team ({0})".format(self.is_default_team_of_user.email)
        return "Team {0} ({1})".format(self.name, self.owner)




#
# Team member, connects people to teams
#
class TeamMembers(models.Manager):

    def filter_for_user(self, user):
        return self.filter(models.Q(team__owner = user) | models.Q(team__members = user)  )

class TeamMember(VideopathBaseModel):

    objects = TeamMembers()

    ROLE_EDITOR = "editor"
    ROLE_ADMIN = "admin"

    TYPE_CHOICES = (
        (ROLE_EDITOR, ROLE_EDITOR),
        (ROLE_ADMIN, ROLE_ADMIN),
    )

    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=20, choices=TYPE_CHOICES, default=ROLE_EDITOR)

#
# Campaign Data to store info about where the user came from
#
class UserCampaignData(VideopathBaseModel):
    user = models.OneToOneField(User, 
                                unique=True, 
                                verbose_name=('user'),
                                related_name='campaign_data'
                                )

    # utm terms
    source = models.CharField(max_length=512, default='', null=True)
    medium = models.CharField(max_length=512, default='', null=True)
    name = models.CharField(max_length=512, default='', null=True)
    content = models.CharField(max_length=512, default='', null=True)
    term = models.CharField(max_length=512, default='', null=True)

    # other info
    country = models.CharField(max_length=512, default='', null=True)
    referrer = models.CharField(max_length=512, default='', null=True)

#
# SalesInfo, saves connection to crm (pipedrive atm)
#
class UserSalesInfo(VideopathBaseModel):
    user = models.OneToOneField(User, 
                                unique=True, 
                                verbose_name=('user'),
                                related_name='sales_info'
                                )
    pipedrive_person_id = models.IntegerField(default=-1, null=True)


#
# remember when users have last been seen
#
class UserActivity(VideopathBaseModel):

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=('user'),
                                related_name='activity')
    last_seen = models.DateTimeField(blank=True, null=True)

#
# remember days on which users where logged in
#
class UserActivityDay(VideopathBaseModel):
    user = models.ForeignKey(User, related_name="user_activity_day")
    day = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "day")

#
# track marketing mails sent to users
#
class AutomatedMail(VideopathBaseModel):

    TYPE_WELCOME = "welcome"
    TYPE_FOLLOW_UP_21 = "follow_up_21"
    TYPE_FOLLOW_UP_42 = "follow_up_42"

    TYPE_CHOICES = (
        (TYPE_WELCOME, TYPE_WELCOME),
        (TYPE_FOLLOW_UP_21, TYPE_FOLLOW_UP_21),
        (TYPE_FOLLOW_UP_42, TYPE_FOLLOW_UP_42),
    )
    user = models.ForeignKey(User, related_name="automated_mails")
    mailtype = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="")


class APIToken(VideopathBaseModel):
    user = models.ForeignKey(User, related_name="api_tokens")
    key = models.CharField(max_length=40, primary_key=True,  blank=True)
    last_used = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(32)
        return super(VideopathBaseModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.key

#
# List of authentication tokens given out to users
#
class AuthenticationToken(VideopathBaseModel):

    user = models.ForeignKey(User, related_name="authentication_tokens")
    key = models.CharField(max_length=40, primary_key=True)
    last_used = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(32)
        return super(AuthenticationToken, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.key

#
# One time authentication tokens, useful in certain conditions, for example our
# annoying http to https switch on the frontend
#
class OneTimeAuthenticationToken(VideopathBaseModel):

    token = models.ForeignKey(
        AuthenticationToken, related_name="onetime_tokens")
    key = models.CharField(max_length=40, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(32)
        return super(OneTimeAuthenticationToken, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.key
