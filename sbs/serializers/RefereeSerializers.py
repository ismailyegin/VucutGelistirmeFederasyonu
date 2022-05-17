from rest_framework import serializers

from sbs.models import Referee
from sbs.models.tvfbf.Coach import Coach


class RefereeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referee
        fields = '__all__'
        depth = 4


class RefereeResponseSerializer(serializers.Serializer):
    data = RefereeSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
