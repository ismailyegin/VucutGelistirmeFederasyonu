
from django.db import models

from sbs.models.ekabis.ConnectionUnit import ConnectionUnit
from sbs.models.ekabis.Company import Company
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog


class YekaContract(BaseModel):

    necesssary_choices = (
        (True, 'Evet '),
        (False, 'Hayır')
    )
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    contract_date=models.DateField(null=True,blank=True)
    contract=models.FileField(null=True,blank=True)
    price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    unit=models.ForeignKey(ConnectionUnit,on_delete=models.DO_NOTHING,null=True,blank=True)
    company=models.ForeignKey(Company,on_delete=models.DO_NOTHING, null=True,blank=True)
    eskalasyonMaxPrice=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)

