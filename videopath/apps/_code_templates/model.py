from django.db import models

from videopath.apps.common.models import VideopathBaseModel

class Model(VideopathBaseModel):

    int_field = models.IntegerField(default=0)
    char_field = models.CharField(max_length=50, blank=True, db_index=True)

    def __unicode__(self):
        return "Name"
      
    class Meta:
        app_label = "app_label"


