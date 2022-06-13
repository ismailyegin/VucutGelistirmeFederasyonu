import enum

import unidecode
from django.contrib.auth.models import User
from django.db import models

from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.City import City
from sbs.models.ekabis.EnumFields import EnumFields
from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.BaseModel import BaseModel


class HavaLevel(BaseModel):
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

    levelType = models.CharField(max_length=128, verbose_name='Leveller', choices=EnumFields.LEVELTYPE.value)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    isActive = models.BooleanField(default=False)
    startDate = models.DateField(null=True, blank=True)
    expireDate = models.DateField(null=True, blank=True, )
    durationDay = models.IntegerField(null=True, blank=True, )
    definition = models.ForeignKey(CategoryItem, on_delete=models.CASCADE, null=True, blank=True)
    definitionChangeUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED)
    dekont = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='Belge ')
    # son eklemeler
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', null=True, blank=True)
    form = models.FileField(upload_to='form/', null=False, blank=False, verbose_name='Form ')
    secretId = models.CharField(null=True, blank=True, max_length=255)
    approval_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s ' % self.branch

    class Meta:
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.dekont:
            self.dekont.name = unidecode.unidecode(self.dekont.name)
        if self.form:
            self.form.name = unidecode.unidecode(self.form.name)
        super(HavaLevel, self).save(*args, **kwargs)
