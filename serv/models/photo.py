import os
from shutil import copy2

from django.conf import settings
from django.db import models
from django.utils import timezone

from serv.utils import calculate_photo_size, mode_photo_size


def files_directory(instance, filename):
    return "photos_user_{0}/{1}".format(instance.owner.id, filename)


class Photo(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photo_owner"
    )
    title = models.CharField(null=False, max_length=255)
    file = models.ImageField(upload_to=files_directory, blank=False)
    view_counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{super().__str__()} | owner: {self.owner} | title: {self.title}"

    def add_view(self):
        self.view_counter += 1
        self.save()

    def min_size_file_save(self):
        filename, file_extension = os.path.splitext(self.file.name)
        file_webp = self.file.path.replace(file_extension, ".webp")
        copy2(self.file.path, file_webp)

        min_file = self.file.path.replace(filename, filename + "_min")
        copy2(self.file.path, min_file)

        mean_width, mean_height = calculate_photo_size(
            self.file.width, self.file.height
        )
        mode_photo_size(min_file, mean_width, mean_height)

    def save(self, *args, **kwargs):
        if not self.pk:
            file = self.file
            self.file = None
            super().save(*args, **kwargs)
            kwargs.pop("force_insert", None)
            self.file = file
        return super().save(*args, **kwargs)
