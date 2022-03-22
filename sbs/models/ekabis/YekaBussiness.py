from sbs.models.ekabis.Company import Company
from sbs.models.ekabis.BaseModel import BaseModel
from django.db import models
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog

class YekaBusiness(BaseModel): #Yekaya ya da yarısmaya ait iş planı
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='İs Planı Tanımı:')
    businessblogs=models.ManyToManyField(YekaBusinessBlog)
    # kazanan firma
    company=models.ForeignKey(Company,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return '%s' % self.name