from rest_framework import serializers

from sbs.models.ekabis.YekaCompetition import YekaCompetition


class YekaCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = YekaCompetition
        fields = '__all__'
        depth = 4




class YekaCompetitionResponseSerializer(serializers.Serializer):
    data = YekaCompetitionSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()