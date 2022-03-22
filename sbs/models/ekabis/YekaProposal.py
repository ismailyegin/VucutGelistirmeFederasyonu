
from django.db import models

from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.Proposal import Proposal
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog
from sbs.models.ekabis.YekaBussiness import YekaBusiness


class YekaProposal(BaseModel):

    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    proposal=models.ManyToManyField(Proposal)



    # startDate=models.DateField(null=True, blank=True)
    # finishDate=models.DateField(null=True,blank=True)
    # preRegistration=models.BooleanField(choices=necesssary_choices,default=False)
    #
    # necessary=models.ManyToManyField(YekaApplicationFileName)
    # companys=models.ManyToManyField(YekaCompany)