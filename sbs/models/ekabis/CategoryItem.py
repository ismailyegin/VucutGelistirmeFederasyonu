from django.db import models
from sbs.models.ekabis.EnumFields import EnumFields
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.tvfbf.Branch import Branch


class CategoryItem(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=255)
    forWhichClazz = models.CharField(blank=False, null=False, max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    isFirst = models.BooleanField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    def locationSet(self, location, deger):
        deger = str(location.name) + "/" + deger
        if not (location.parent):
            return '%s' % (str(deger))
        else:
            location = CategoryItem.objects.get(pk=location.parent_id)
            return self.locationSet(location, deger)

    def __str__(self):
        if self.parent == None:
            return '%s' % (self.name)
        else:
            location = CategoryItem.objects.get(pk=self.parent_id)
            return '%s' % (self.locationSet(location, '') + self.name)

    # class Meta:
    #     default_permissions = ()
    #     db_table = 'categoryitem'
    #     managed = False
