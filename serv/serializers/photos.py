import os
from urllib.parse import urljoin

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from serv.models.photo import Photo
from serv.serializers.users import CreateUserSerializer


class PhotoSerializer(serializers.ModelSerializer):
    owner = CreateUserSerializer(read_only=True)
    photo_webp = serializers.SerializerMethodField(read_only=True)
    min_size_photo = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Photo
        fields = (
            "id",
            "title",
            "file",
            "owner",
            "created_at",
            "view_counter",
            "min_size_photo",
            "photo_webp",
        )
        read_only_fields = (
            "created_at",
            "view_counter",
            "min_size_photo",
            "photo_webp",
        )

    def validate(self, data):
        request = self.context["request"]
        if request.method.upper() == "POST":
            data["owner"] = request.user
        return data

    def validate_file(self, file):
        filename, file_extension = os.path.splitext(file.name)
        if file_extension in [".png", ".jpg", ".jpeg"] and file.size <= 5242880:
            return file
        raise ValidationError(
            "Формат фото должен быть PNG (*.png), JPEG (*.jpg, *.jpeg)"
        )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key in {"title"}:
                continue
            if getattr(instance, key) != value:
                raise ValidationError(f'Change field "{key}" forbidden.')

        return super().update(instance, validated_data)

    def get_photo_webp(self, obj):
        filename, file_extension = os.path.splitext(obj.file.name)
        min_file = obj.file.url.replace(file_extension, ".webp")
        return urljoin("http://127.0.0.1:8000/", min_file)

    def get_min_size_photo(self, obj):
        filename, file_extension = os.path.splitext(obj.file.name)
        min_file = obj.file.url.replace(filename, filename + "_min")
        return urljoin("http://127.0.0.1:8000/", min_file)
