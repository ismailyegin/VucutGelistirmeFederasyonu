from django.db import models
from sbs.models.havaspor.BaseModel import BaseModel
class File(BaseModel):
    file = models.FileField()