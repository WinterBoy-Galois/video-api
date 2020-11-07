from django.db import models

from videopath.apps.users.models import Team

from videopath.apps.common.models import VideopathBaseModel


class Integration(VideopathBaseModel):

	# owner
    team = models.ForeignKey(Team, related_name='integrations')

    SERVICE_CHOICES = (
    	('mailchimp', 'mailchimp'),
        ('vimeo', 'vimeo'),
        ('brightcove', 'brightcove')
    )

    service = models.CharField(max_length=255, default='', choices=SERVICE_CHOICES)

    # settings 
    credentials = models.CharField(max_length=2048, blank=True)
    settings = models.CharField(max_length=2048, blank=True)

    # meta settings
    class Meta:
        unique_together = ("team", "service")