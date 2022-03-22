from django.db import models

from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog



class Newspaper(BaseModel):
    business = models.ForeignKey(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    listingDate=models.DateField(null=True, blank=True)
    newspaperCount=models.CharField(max_length=120,blank=True, null=True)
    newspapwerText=models.TextField(blank=True, null=True)
    file=models.FileField()
