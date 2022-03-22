from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.FactoryFileName import FactoryFileName


class FactoryFile(BaseModel):
    file = models.FileField(upload_to='fabrika-dokumani/', null=False, blank=False, verbose_name='Fabrika Dokümanı')
    name = models.ForeignKey(FactoryFileName, null=False, blank=False, on_delete=models.DO_NOTHING)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.name