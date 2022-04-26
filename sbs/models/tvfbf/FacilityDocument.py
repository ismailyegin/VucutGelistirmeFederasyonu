from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.tvfbf.DocumentName import DocumentName


class FacilityDocument(BaseModel):
    name = models.ForeignKey(DocumentName,blank=True, null=True, max_length=255, verbose_name='Belge Adı',on_delete=models.CASCADE)
    file = models.FileField(upload_to='tesis-belge/', null=True, blank=True)

    def __str__(self):
        return '%s' % self.name
