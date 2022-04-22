from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel


class DocumentName(BaseModel):
    name = models.CharField(blank=True, null=True, max_length=255, verbose_name='Belge Adı')

    def __str__(self):
        return '%s' % self.name
