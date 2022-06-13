import unidecode
from django.db import models

from sbs.models.tvfbf.BaseModel import BaseModel
from sbs.models.tvfbf.Coach import Coach


class CoachApplication(BaseModel):
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

    status = models.CharField(max_length=128, verbose_name='Kayıt Durumu', choices=STATUS_CHOICES, default=WAITED)
    coach = models.ForeignKey(Coach, on_delete=models.DO_NOTHING, null=False, blank=False)
    dekont = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='coachApplication ')

    def __str__(self):
        return '%s ' % self.coach

    class Meta:
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.dekont:
            self.dekont.name = unidecode.unidecode(self.dekont.name)
        super(CoachApplication, self).save(*args, **kwargs)
