from django.contrib.auth.models import User
from django.db import models

from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Person import Person
from sbs.models.havaspor.BaseModel import BaseModel
from sbs.models.havaspor.ClubRole import ClubRole


class SportClubUser(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(ClubRole, on_delete=models.CASCADE, verbose_name='Üye Rolü')
    dataAccessControl = models.BooleanField(blank=True, null=True, default=False)

    oldpk = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    # class Meta:
    #     default_permissions = ()
