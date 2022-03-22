from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaApplicationFileName import YekaApplicationFileName

class YekaApplicationFile(BaseModel):
    filename = models.ForeignKey(YekaApplicationFileName,on_delete=models.DO_NOTHING)
    file=models.FileField(null=True,blank=True)
