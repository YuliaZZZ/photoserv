import os
import subprocess
from datetime import datetime
from shutil import copy2

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

from app.celery import app
from serv.models.photo import Photo


@app.task(name="send_notification", bind=True, max_retries=3, queue="app_queue")
def send_notification(self, subject, message, user_id):
    user = User.objects.get(id=user_id)
    try:
        send_mail(subject=subject, message=message, from_email=user.email)
    except Exception:
        self.retry(countdown=120)


@app.task(name="create_toplist_video", bind=True, max_retries=1, queue="app_queue")
def create_toplist_video(self):
    try:
        photo_list = Photo.objects.all().order_by("-view_counter")[:10]

        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, "top_photos_lists")):
            os.mkdir(
                os.path.join(settings.MEDIA_ROOT, "top_photos_lists"),
                mode=0o700,
                dir_fd=None,
            )

        image_folder = os.path.join(
            settings.MEDIA_ROOT,
            "top_photos_lists",
            f"toplist_{datetime.date(timezone.now())}",
        )

        if not os.path.isdir(image_folder):
            os.mkdir(image_folder, mode=0o700, dir_fd=None)

        x = 0
        for file in [i.file for i in photo_list]:
            x += 1
            copy2(file.path, os.path.join(image_folder, f"image_{x}.jpeg"))

        video_name = os.path.join(image_folder, "top_photos.webm")

        ffmpeg_command = [
            "ffmpeg",
            "-f",
            "image2",
            "-i",
            f"{image_folder}/image_%d.jpeg",
            video_name,
        ]
        subprocess.call(ffmpeg_command)
    except Exception:
        self.retry(countdown=60)
