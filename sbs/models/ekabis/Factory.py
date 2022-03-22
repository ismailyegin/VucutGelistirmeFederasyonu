from django.db import models
from unicode_tr import unicode_tr

from sbs.models.ekabis.FactoryFile import FactoryFile
from sbs.models.ekabis.BaseModel import BaseModel


class Factory(BaseModel):
    date = models.DateField()
    name = models.CharField(max_length=120, null=False, blank=False)
    file = models.ManyToManyField(FactoryFile)

    def __str__(self):
        return '%s' % self.name
    def save(self, force_insert=False, force_update=False):
        if self.name:
            self.name = unicode_tr(self.name).upper()

        super(Factory, self).save(force_insert, force_update)
