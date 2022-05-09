from rest_framework import serializers

from sbs.models.ekabis.Permission import Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        depth = 4


class PermissionResponseSerializer(serializers.Serializer):
    data = PermissionSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
