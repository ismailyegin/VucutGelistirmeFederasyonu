from django.db import models

from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.Factory import Factory
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog


class YekaFactory(BaseModel):
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    factory = models.ManyToManyField(Factory)
