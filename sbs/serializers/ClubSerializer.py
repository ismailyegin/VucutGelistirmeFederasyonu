from rest_framework import serializers
from sbs.models.tvfbf.Club import Club


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'
        depth = 3


class ClubResponseSerializer(serializers.Serializer):
    data = ClubSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
