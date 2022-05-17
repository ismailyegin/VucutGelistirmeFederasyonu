from rest_framework import serializers

from sbs.models.tvfbf.Coach import Coach


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'
        depth = 4


class CoachResponseSerializer(serializers.Serializer):
    data = CoachSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
