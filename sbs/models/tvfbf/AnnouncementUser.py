from django.contrib.auth.models import User
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.tvfbf.Announcement import Announcement


class AnnouncementUser(BaseModel):
    announcement = models.ForeignKey(Announcement, on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    isShow = models.BooleanField(default=False)
    isRead = models.BooleanField(default=False)
    readDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.user.get_full_name()
