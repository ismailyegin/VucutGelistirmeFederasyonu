from rest_framework import serializers

from sbs.models.ekabis.Neighborhood import Neighborhood


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = '__all__'
        depth = 3
