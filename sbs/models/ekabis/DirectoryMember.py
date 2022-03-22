from django.contrib.auth.models import User
from django.db import models

from sbs.models.ekabis.DirectoryCommission import DirectoryCommission
from sbs.models.ekabis.DirectoryMemberRole import DirectoryMemberRole
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.BaseModel import BaseModel


class DirectoryMember(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.DO_NOTHING)
    communication = models.OneToOneField(Communication, on_delete=models.DO_NOTHING)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(DirectoryMemberRole, on_delete=models.DO_NOTHING, verbose_name='Üye Rolü')
    commission = models.ForeignKey(DirectoryCommission, on_delete=models.DO_NOTHING, verbose_name='Kurulu')


    class Meta:
        default_permissions = ()
