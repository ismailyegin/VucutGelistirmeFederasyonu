from rest_framework import serializers

from sbs.models.tvfbf.Announcement import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        depth = 3