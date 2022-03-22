from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.ProduceAmount import ProduceAmount
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog


class YekaProduceAmount(BaseModel):
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING) #iş planı
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING) #iş planına ait iş bloğu
    amount = models.ManyToManyField(ProduceAmount, null=True, blank=True, verbose_name='Üretim Miktarı')
