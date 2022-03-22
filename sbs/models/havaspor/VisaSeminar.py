from django.db import models

from sbs.models.havaspor.Branch import Branch
from sbs.models.havaspor.BaseModel import BaseModel
from sbs.models.havaspor.Coach import Coach
from sbs.models.havaspor.Referee import Referee
from sbs.models.ekabis.EnumFields import EnumFields
from sbs.models.havaspor.CoachApplication import CoachApplication
from sbs.models.havaspor.RefereeApplication import RefereeApplication


class VisaSeminar(BaseModel):
    WAITED = 'Beklemede'
    APPROVED = 'Onaylandı'
    PROPOUND = 'Onaya Gönderildi'
    DENIED = 'Reddedildi'

    STATUS_CHOICES = (
        (APPROVED, 'Onaylandı'),
        (PROPOUND, 'Onaya Gönderildi'),
        (DENIED, 'Reddedildi'),
        (WAITED, 'Beklemede'),
    )

    name = models.CharField(blank=False, null=False, max_length=1000)
    startDate = models.DateTimeField()
    finishDate = models.DateTimeField()
    location = models.CharField(blank=False, null=False, max_length=1000)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, verbose_name='branş')
    status = models.CharField(max_length=128, verbose_name='Kayıt Durumu', choices=STATUS_CHOICES, default=WAITED)
    coach = models.ManyToManyField(Coach, related_name='coach')
    coachApplication = models.ManyToManyField(CoachApplication, related_name='coachApplication')
    refereeApplication = models.ManyToManyField(RefereeApplication, related_name='refereeApplication')
    referee = models.ManyToManyField(Referee, related_name='referee')
    forWhichClazz = models.CharField(blank=False, null=False, max_length=255)
    year = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
