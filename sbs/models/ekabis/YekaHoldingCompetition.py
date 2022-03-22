from django.db import models

from sbs.models.ekabis.ConnectionUnit import ConnectionUnit
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog

#Yarışmanın yapılması iş bloğunda Yarışma Tavan fiyatı için birim kayıt edilmekte
class YekaHoldingCompetition(BaseModel):
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    unit=models.ForeignKey(ConnectionUnit,on_delete=models.DO_NOTHING,null=True,blank=True)
    max_price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)

