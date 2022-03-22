from django.contrib.auth.models import User
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog


class ExtraTime(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.IntegerField()
    business = models.ForeignKey(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    file = models.FileField(null=True, blank=True) # extra zaman belgesi
    time_type = models.CharField(null=True, blank=True, max_length=100)
    definition = models.CharField(null=True, blank=True, max_length=250)
    new_date = models.DateField(null=True, blank=True)  # added_date + time = isin yapılma tarihi
    old_date = models.DateField(null=True, blank=True)  # eski işin yapılma tarihi
    added_date = models.DateField(null=True, blank=True)  # bu tarihten itibaren süre eklenir
