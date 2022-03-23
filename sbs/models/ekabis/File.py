from django.db import models
from sbs.models.tvfbf.BaseModel import BaseModel
class File(BaseModel):
    file = models.FileField()