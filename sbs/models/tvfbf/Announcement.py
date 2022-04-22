from django.contrib.auth.models import Group
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel


class Announcement(BaseModel):
    title = models.CharField(blank=True, null=True, max_length=255, verbose_name='Duyuru Başlığı')
    text = models.TextField(blank=True, null=True, verbose_name='Duyuru Yazısı')
    group = models.ManyToManyField(Group, verbose_name='Duyuru Grupları')
    startDate = models.DateField(blank=True, null=True)
    finishDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.title
