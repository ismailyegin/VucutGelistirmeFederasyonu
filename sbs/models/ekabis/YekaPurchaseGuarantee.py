from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog


class YekaPurchaseGuarantee(BaseModel):
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    time = models.IntegerField(null=True, blank=True, verbose_name='Süre')
    total_quantity = models.IntegerField(null=True, blank=True, verbose_name='Toplam Miktar(GWh)')
    type = models.CharField(null=True, blank=True, max_length=100)
