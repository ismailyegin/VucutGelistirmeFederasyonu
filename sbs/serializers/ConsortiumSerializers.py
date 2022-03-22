from rest_framework import serializers

from sbs.models.ekabis.ConsortiumCompany import ConsortiumCompany


class ConsortiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsortiumCompany
        fields = '__all__'
        depth = 3