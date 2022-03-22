from rest_framework import serializers

from sbs.models.ekabis.NotificationUser import NotificationUser


class NotificationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationUser
        fields = '__all__'
        depth = 3