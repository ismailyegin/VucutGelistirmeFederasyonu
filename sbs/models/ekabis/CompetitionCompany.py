from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.Company import Company


class CompetitionCompany(BaseModel):

    price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    company=models.ForeignKey(Company,on_delete=models.DO_NOTHING,null=False,blank=False)
