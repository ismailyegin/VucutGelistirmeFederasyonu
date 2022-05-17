from rest_framework import serializers

from sbs.models import SportFacility
from sbs.models.tvfbf.Coach import Coach


class SportFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SportFacility
        fields = '__all__'
        depth = 4


class SportFacilityResponseSerializer(serializers.Serializer):
    data = SportFacilitySerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
