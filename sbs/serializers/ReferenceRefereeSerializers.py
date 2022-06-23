from rest_framework import serializers

from sbs.models.tvfbf.ReferenceReferee import ReferenceReferee


class ReferenceRefereeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceReferee
        fields = '__all__'
        depth = 4


class ReferenceRefereeResponseSerializer(serializers.Serializer):
    data = ReferenceRefereeSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
