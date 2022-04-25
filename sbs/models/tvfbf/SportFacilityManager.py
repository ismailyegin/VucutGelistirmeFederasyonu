from django.db import models

from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Person import Person
from sbs.models.tvfbf.BaseModel import BaseModel
from sbs.models.tvfbf.Branch import Branch


class SportFacilityManager(BaseModel):
    type = (
        (True, 'Gerçek Kişi'),
        (False, 'Tüzel Kişi'),
    )
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True, blank=True)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ManyToManyField(Branch)
    role=models.CharField(max_length=250,null=True,blank=True,verbose_name='Görev')
    personalityType=models.BooleanField(default=True, choices=type)

    def __str__(self):
        return '%s ' % self.person.user.get_full_name()
