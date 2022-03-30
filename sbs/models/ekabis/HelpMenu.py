from django.db import models

from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.BaseModel import BaseModel


class HelpMenu(BaseModel):
    text = models.TextField(blank=False, null=False, verbose_name='Açıklama')
    url = models.OneToOneField(Permission,verbose_name='URL', on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s ' % self.url
