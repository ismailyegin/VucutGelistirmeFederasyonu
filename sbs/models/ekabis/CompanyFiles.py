from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.CompanyFileNames import CompanyFileNames
class CompanyFiles(BaseModel):

    filename=models.ForeignKey(CompanyFileNames,on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='company/', null=True, blank=True,verbose_name='company_files')

    def __str__(self):
        return '%s' % self.filename