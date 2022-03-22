from django.db import models

from sbs.models.ekabis.YekaCompetitionEskalasyon import YekaCompetitionEskalasyon
from sbs.models.ekabis.Eskalasyon import Eskalasyon
from sbs.models.ekabis.BaseModel import BaseModel


class YekaCompetitionEskalasyon_eskalasyon(BaseModel):
    eskalasyon_info = models.ForeignKey(Eskalasyon, null=True, blank=True,
                                        on_delete=models.DO_NOTHING)  # Formuldeki her bir alt formüllerin sonuç ve bilgileri
    yeka_competition_eskalasyon = models.ForeignKey(YekaCompetitionEskalasyon, on_delete=models.DO_NOTHING, null=True,
                                                    blank=True)  # yeka yarışması eskalasyonu
