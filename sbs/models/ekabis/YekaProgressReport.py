from django.db import models

from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.ProgressReport import ProgressReport
from sbs.models.ekabis.BaseModel import BaseModel


class YekaProgressReport(BaseModel):
    competition = models.OneToOneField(YekaCompetition, on_delete=models.DO_NOTHING)
    progressReport = models.ManyToManyField(ProgressReport)
