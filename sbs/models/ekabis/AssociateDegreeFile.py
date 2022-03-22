from django.db import models

from sbs.models.ekabis.AssociateDegreeFileName import AssociateDegreeFileName
from sbs.models.ekabis.BaseModel import BaseModel


class AssociateDegreeFile(BaseModel):
    file = models.FileField(upload_to='onlisans-sureci/', null=False, blank=False,
                            verbose_name='Önlisans Süreci Dokümanı')
    name = models.ForeignKey(AssociateDegreeFileName, null=False, blank=False, on_delete=models.DO_NOTHING)
    date = models.DateField(null=True, blank=True)
