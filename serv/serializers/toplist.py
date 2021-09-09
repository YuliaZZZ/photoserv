import datetime
from urllib.parse import urljoin

from django.utils import timezone
from rest_framework import serializers


class TopListSerializer(serializers.Serializer):
    toplist_file = serializers.SerializerMethodField(
        default=serializers.FileField(), read_only=True
    )

    def get_toplist_file(self, obj):
        now = datetime.datetime.date(timezone.now())
        folder = f"http://127.0.0.1:8000/media/top_photos_lists/toplist_{now}/"
        return urljoin(folder, "top_photos.webm")
