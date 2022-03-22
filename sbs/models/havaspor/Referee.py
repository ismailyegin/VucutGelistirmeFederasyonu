from django.db import models

from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Person import Person
from sbs.models.havaspor.HavaLevel import HavaLevel
from sbs.models.havaspor.BaseModel import BaseModel
from sbs.models.havaspor.Branch import Branch


class Referee(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    nufusCuzdani = models.FileField(upload_to='referee/', null=True, blank=True, verbose_name='Nufüs Cüzdanı',max_length=500)
    diploma = models.FileField(upload_to='referee/', null=True, blank=True, verbose_name='Diploma',max_length=500)
    sabikaKaydi = models.FileField(upload_to='referee/', null=True, blank=True, verbose_name='Sabıka Kaydı',max_length=500)
    cezaYazisi = models.FileField(upload_to='referee/', null=True, blank=True, verbose_name='Ceza Yazısı',max_length=500)
    saglikBeyanFormu = models.FileField(upload_to='referee/', null=True, blank=True, verbose_name='Sağlık Beyan Formu',max_length=500)
    hakemBilgiFormu = models.FileField(upload_to='referee/', null=True, blank=True, verbose_name='Hakem Bilgi Formu',max_length=500)
    grades = models.ManyToManyField(HavaLevel, related_name='Refereegrades')
    visa = models.ManyToManyField(HavaLevel, related_name='Refereevisa')
    infoLevel = models.BooleanField(default=True, null=True, blank=True)
    infoStatus = models.BooleanField(default=True, null=True, blank=True)
    secretId = models.CharField(max_length=250, null=True, blank=True)


    # grades = models.ManyToManyField(Level, related_name='CoachGrades')
    # visa = models.ManyToManyField(Level, related_name='CoachVisa')

    def __str__(self):
        return '%s %s' % (self.person.user.first_name, self.person.user.last_name)
