from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel

from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Communication import Communication


class Employee(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.DO_NOTHING, db_column='person', null=False, blank=False)
    communication = models.OneToOneField(Communication, on_delete=models.DO_NOTHING, db_column='communication')

    def __str__(self):
        return '%s' % self.person.user.get_full_name()

    class Meta:
        ordering = ['pk']
        default_permissions = ()
