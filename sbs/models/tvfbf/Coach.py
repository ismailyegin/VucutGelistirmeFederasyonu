from django.db import models
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Person import Person
from sbs.models.tvfbf.HavaLevel import HavaLevel
from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.BaseModel import BaseModel


class Coach(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    branch = models.ManyToManyField(Branch)
    nufusCuzdani = models.FileField(null=True, blank=True, verbose_name='Nufüs Cüzdanı')
    diploma = models.FileField(null=True, blank=True, verbose_name='Diploma')
    sabikaKaydi = models.FileField(null=True, blank=True, verbose_name='Sabıka Kaydı')
    cezaYazisi = models.FileField(null=True, blank=True, verbose_name='Ceza Yazısı')
    saglikBeyanFormu = models.FileField(null=True, blank=True, verbose_name='Sağlık Beyan Formu')
    antrenorBelgesi = models.FileField(null=True, blank=True, verbose_name='Antrenör Belgesi')
    infoLevel = models.BooleanField(default=True, null=True, blank=True)
    infoStatus = models.BooleanField(default=True, null=True, blank=True)

    grades = models.ManyToManyField(HavaLevel, related_name='CoachGrades')
    visa = models.ManyToManyField(HavaLevel, related_name='CoachVisa')


    def __str__(self):
        return '%s %s' % (self.person.user.first_name, self.person.user.last_name)

    # class Meta:
    #     ordering = ['pk']
    #     default_permissions = ()
