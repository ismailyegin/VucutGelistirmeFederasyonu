from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog
from sbs.models.ekabis.YekaApplicationFileName import YekaApplicationFileName


class CompetitionApplication(BaseModel):
    necesssary_choices = (
        (True, 'Evet '),
        (False, 'Hayır')
    )
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING,null=True,blank=True)
    startDate = models.DateField(null=True, blank=True)
    finishDate = models.DateField(null=True, blank=True)
    preRegistration = models.BooleanField(choices=necesssary_choices, default=False)
    necessary = models.ManyToManyField(YekaApplicationFileName)

