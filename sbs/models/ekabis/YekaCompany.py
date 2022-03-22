from django.db import models

from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.ConnectionRegion import ConnectionRegion
from sbs.models.ekabis.Yeka import Yeka
from sbs.models.ekabis.Company import Company
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.CompetitionApplication import CompetitionApplication
from sbs.models.ekabis.YekaApplicationFile import YekaApplicationFile


class YekaCompany(BaseModel):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(null=True, blank=True, default=True)
    files = models.ManyToManyField(YekaApplicationFile)
    # price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
    connection_region = models.ForeignKey(ConnectionRegion, on_delete=models.DO_NOTHING, null=True, blank=True)
    competition = models.ForeignKey(YekaCompetition, on_delete=models.DO_NOTHING, null=True, blank=True)
    application = models.ForeignKey(CompetitionApplication, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return '%s ' % self.company.name
