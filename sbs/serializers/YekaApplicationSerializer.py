from rest_framework import serializers

from sbs.models.ekabis.CompetitionApplication import CompetitionApplication


class YekaApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionApplication
        fields = '__all__'
        depth = 3