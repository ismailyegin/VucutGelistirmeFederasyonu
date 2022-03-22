from django.db import models

from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.Institution import Institution

class ProposalActive(BaseModel):
    business=models.ForeignKey(YekaBusiness,on_delete=models.DO_NOTHING)
    institution=models.ForeignKey(Institution,on_delete=models.DO_NOTHING)
    is_active=models.BooleanField(default=False)
