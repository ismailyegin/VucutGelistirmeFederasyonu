from django.db import models
from sbs.models.ekabis.Employee import Employee
from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.BaseModel import BaseModel


class YekaCompetitionPersonHistory(BaseModel):

    competition = models.ForeignKey(YekaCompetition, on_delete=models.DO_NOTHING, verbose_name='competition')
    person = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, verbose_name='personel')
    is_active = models.BooleanField(default=False)