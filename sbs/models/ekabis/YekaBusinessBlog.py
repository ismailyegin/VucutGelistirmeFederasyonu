from django.db import models

from sbs.models.ekabis.Company import Company
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.BusinessBlog import BusinessBlog
from sbs.models.ekabis.YekaBusinessBlogParemetre import YekaBusinessBlogParemetre


class YekaBusinessBlog(BaseModel):
    INDEFINETE_CHOICES = (
        (True, 'Süresiz '),
        (False, 'Süreli')
    )
    businessblog = models.ForeignKey(BusinessBlog, on_delete=models.DO_NOTHING, null=True, blank=True) #iş planında bulunan bir bloğun sabit bilgileri
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='business_parent', null=True, blank=True)
    startDate = models.DateTimeField(null=True, blank=True)
    finisDate = models.DateTimeField(null=True, blank=True)
    businessTime = models.IntegerField(null=True, blank=True)
    time_type = models.CharField(null=True, blank=True, max_length=100)
    status = models.CharField(max_length=100, null=True, blank=True, default='Başlanmadı')
    sorting = models.IntegerField(default=0)
    companies = models.ManyToManyField(Company)
    parameter = models.ManyToManyField(YekaBusinessBlogParemetre, null=True, blank=True) #dinamik parametre bilgileri
    indefinite = models.BooleanField(default=False, choices=INDEFINETE_CHOICES)
    explanation = models.CharField(max_length=250,null=True, blank=True)
    dependence_parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='depence_parent', null=True,
                                          blank=True)
    child_block = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='business_child', null=True, blank=True)

    completion_date = models.DateTimeField(null=True, blank=True, verbose_name='Tamamlanma Tarihi')

    def __str__(self):
        return '%s' % (self.businessblog.name)
