
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel


class Permission(BaseModel):
    yeka = 'Yeka'
    referee = 'Hakem'
    coach = 'Antrenör'
    main = 'Anasayfa'
    settings = 'Ayarlar'
    other = 'Digerleri'

    Type = (

        (referee, 'Hakem'),
        (coach, 'Antrenör'),
        (main, 'Anasayfa'),
        (settings, 'Ayarlar'),
        (other, 'Digerleri'),

    )
    name = models.CharField( max_length=255,blank=True,null=True)
    model = models.CharField( max_length=100,blank=True,null=True)
    codename = models.CharField( max_length=300,blank=False,null=False)
    codeurl = models.CharField( max_length=300,blank=False,null=False)
    parent=models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    group=models.CharField(max_length=100,blank=True,null=True,choices=Type)
    def __str__(self):
        return '%s ' % self.name +'('+self.codename+')'

    class Meta:
        default_permissions = ()
