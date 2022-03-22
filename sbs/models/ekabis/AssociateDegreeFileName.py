
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel

class AssociateDegreeFileName(BaseModel):
    name = models.CharField(blank=True, null=True, max_length=250)

    def __str__(self):
        return '%s ' % self.name



