
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel

class YekaApplicationFileName(BaseModel):
    filename = models.CharField(blank=True, null=True, max_length=250)



