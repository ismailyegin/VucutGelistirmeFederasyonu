from django.contrib.auth.models import User
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
class Institution(BaseModel):
    name=models.CharField(max_length=200,null=False,blank=False)
