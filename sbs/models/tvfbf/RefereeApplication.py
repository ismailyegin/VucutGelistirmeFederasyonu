from django.db import models

from sbs.models.tvfbf.BaseModel import BaseModel
from sbs.models.tvfbf.Referee import Referee


class RefereeApplication(BaseModel):
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
    referee = models.ForeignKey(Referee, on_delete=models.DO_NOTHING, null=False, blank=False)
    dekont = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='refereeApplication ')

    def __str__(self):
        return '%s ' % self.referee

    class Meta:
        default_permissions = ()
