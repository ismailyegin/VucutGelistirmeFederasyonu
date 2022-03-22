from django.db import models

from sbs.models.ekabis.ConnectionRegion import ConnectionRegion
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.Yeka import Yeka


class YekaConnectionRegion(BaseModel):
    connectionRegion = models.ForeignKey(ConnectionRegion, null=True, blank=True, on_delete=models.DO_NOTHING)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
