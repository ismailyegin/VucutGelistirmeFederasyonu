from django.db import models

from sbs.models.ekabis.BaseModel import BaseModel


class Coordinate(BaseModel):
    y = models.DecimalField(blank=False, null=False, max_digits=9, decimal_places=6)
    x = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=6)

    def __str__(self):
        return '%s %s %s' % (self.x, '-', self.y)
