from rest_framework import serializers

from sbs.models import ReferenceCoach
from sbs.models.tvfbf.Coach import Coach


class ReferenceCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceCoach
        fields = '__all__'
        depth = 4


class ReferenceCoachResponseSerializer(serializers.Serializer):
    data = ReferenceCoachSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
