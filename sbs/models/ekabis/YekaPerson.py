from django.db import models




from sbs.models.ekabis.Employee import Employee

from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.Yeka import Yeka


class YekaPerson(BaseModel):
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.DO_NOTHING)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s ' % self.employee.person.user.get_full_name()

    task_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)



