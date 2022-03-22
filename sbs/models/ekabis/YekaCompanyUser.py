
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog
from sbs.models.ekabis.YekaUser import YekaUser

class YekaCompanyUser(BaseModel):

    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    companyuser=models.ManyToManyField(YekaUser)

