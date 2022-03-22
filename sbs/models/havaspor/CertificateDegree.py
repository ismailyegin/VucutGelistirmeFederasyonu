from django.db import models

from sbs.models.havaspor.BaseModel import BaseModel


class CertificateDegree(BaseModel):
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

    name = models.TextField(null=True, blank=True, verbose_name='Sertifika Adı')
    certificateDate = models.DateField(blank=True, null=True)
    educationPlace = models.CharField(null=True, blank=True, max_length=255)
    status = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED)
    reddetwhy = models.CharField(blank=True, null=True, max_length=255)


    def __str__(self):
        return '%s ' % self.name
