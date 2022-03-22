from django.db import models

from sbs.models.ekabis.Proposal import Proposal
from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.BaseModel import BaseModel

#Aday Yekaya ait alt yeka belirlenmesi
class ProposalSubYeka(BaseModel):
    sub_yeka = models.ForeignKey(YekaCompetition, on_delete=models.DO_NOTHING, null=True, blank=True)
    proposal = models.OneToOneField(Proposal, on_delete=models.DO_NOTHING, null=True, blank=True)
