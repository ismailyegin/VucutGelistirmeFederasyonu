from rest_framework import serializers

from sbs.models.ekabis.Proposal import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'
        depth = 3


class ProposalResponseSerializer(serializers.Serializer):
    data = ProposalSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
