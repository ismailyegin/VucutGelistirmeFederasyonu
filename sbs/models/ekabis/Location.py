from django.db import models

from sbs.models.ekabis.Neighborhood import Neighborhood
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.City import City
from sbs.models.ekabis.District import District


class Location(BaseModel):
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, verbose_name='İl', db_column='city', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, null=True, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, max_length=120, null=True, blank=True, on_delete=models.DO_NOTHING)
    parcel = models.CharField(max_length=250,null=True, blank=True)
