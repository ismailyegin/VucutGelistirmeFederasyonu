from random import choices
from django.contrib.auth.models import Group
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.Permission import Permission


class PermissionGroup(BaseModel):
    permissions = models.ForeignKey(Permission, verbose_name='permissions', blank=True, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, verbose_name='group', blank=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
