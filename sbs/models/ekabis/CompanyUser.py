from django.contrib.auth.models import User
from django.db import models

from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.BaseModel import BaseModel


class CompanyUser(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.DO_NOTHING, null=True, blank=True)
    communication = models.OneToOneField(Communication, on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    authorization_period_start = models.DateField(blank=True, null=True)
    authorization_period_finish = models.DateField(blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return '%s ' % self.person.user.get_full_name()
