import random
import re
import string 
import copy

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

# base model for all classes
class VideopathBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            if self.id == None:
                newid = random.randint(147483647, 2147483647)
                while self.__class__.objects.filter(pk=newid).exists():
                    newid = random.randint(147483647, 2147483647)
                self.id = newid
        except Exception:
            pass
        super(VideopathBaseModel, self).save(*args, **kwargs)

    def generate_key(self, length=16):
            return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(length))

    def reload(self):
        return self.__class__.objects.get(pk=self.pk)

    def duplicate(self):
        duplicate = copy.copy(self)
        duplicate.pk = None
        duplicate.save()
        return duplicate

    class Meta:
        abstract = True

# color field
color_re = re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
validate_color = RegexValidator(
    color_re, _(u'Enter a valid color.'), 'invalid')

class ColorField(models.CharField):
    default_validators = [validate_color]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)
        