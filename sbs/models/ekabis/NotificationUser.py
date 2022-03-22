from django.contrib.auth.models import User
from django.db import models

from sbs.models.ekabis.Notification import Notification
from sbs.models.ekabis.BaseModel import BaseModel


class NotificationUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    read_date = models.DateField(null=True, blank=True)
    notification = models.ForeignKey(Notification, on_delete=models.DO_NOTHING,null=True,blank=True)
