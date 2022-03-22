

from django.db import models

from sbs.models.ekabis.Employee import Employee
from sbs.models.ekabis.Yeka import Yeka
from sbs.models.ekabis.BaseModel import BaseModel


class YekaPersonHistory(BaseModel):

    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, verbose_name='yeka')
    person = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, verbose_name='personel')
    is_active = models.BooleanField(default=False)
