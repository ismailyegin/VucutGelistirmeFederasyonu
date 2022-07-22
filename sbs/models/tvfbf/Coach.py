import unidecode
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
    sgk = models.FileField(null=True, blank=True, verbose_name='SGK Belgesi')

    grades = models.ManyToManyField(HavaLevel, related_name='CoachGrades')
    visa = models.ManyToManyField(HavaLevel, related_name='CoachVisa')

    form = models.FileField(upload_to='form/', null=True, blank=True,
                            verbose_name='Form ')  # Antrenör sözleşme belgesi

    def __str__(self):
        return '%s %s' % (self.person.user.first_name, self.person.user.last_name)

    def save(self, *args, **kwargs):
        if self.nufusCuzdani:
            self.nufusCuzdani.name = unidecode.unidecode(self.nufusCuzdani.name)
        if self.diploma:
            self.diploma.name = unidecode.unidecode(self.diploma.name)
        if self.sabikaKaydi:
            self.sabikaKaydi.name = unidecode.unidecode(self.sabikaKaydi.name)
        if self.cezaYazisi:
            self.cezaYazisi.name = unidecode.unidecode(self.cezaYazisi.name)
        if self.saglikBeyanFormu:
            self.saglikBeyanFormu.name = unidecode.unidecode(self.saglikBeyanFormu.name)
        if self.antrenorBelgesi:
            self.antrenorBelgesi.name = unidecode.unidecode(self.antrenorBelgesi.name)
        if self.sgk:
            self.sgk.name = unidecode.unidecode(self.sgk.name)
        if self.form:
            self.form.name = unidecode.unidecode(self.form.name)
        super(Coach, self).save(*args, **kwargs)

    # class Meta:
    #     ordering = ['pk']
    #     default_permissions = ()
