from rest_framework import serializers

from sbs.models.ekabis.YekaCompetitionEskalasyon import YekaCompetitionEskalasyon


class YekaCompetitionEskalasyonSerializer(serializers.ModelSerializer):
    class Meta:
        model = YekaCompetitionEskalasyon
        fields = '__all__'
        depth = 3