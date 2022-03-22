from django.db import models

from sbs.models.ekabis.Company import Company
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.Yeka import Yeka


class YekaCompanyHistory(BaseModel):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.DO_NOTHING)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s ' % self.company.name
