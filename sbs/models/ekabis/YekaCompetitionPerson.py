from django.db import models

from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.Employee import Employee

from sbs.models.ekabis.BaseModel import BaseModel


class YekaCompetitionPerson(BaseModel):
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.DO_NOTHING)
    competition = models.ForeignKey(YekaCompetition, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    task_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return '%s %s %s ' % (
            self.employee.person.user.first_name, self.employee.person.user.last_name, ' - ')