import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner", related_name="album")
    name = models.CharField(max_length=256, verbose_name="Name")

    class Meta:
        verbose_name_plural = "Albums"

    def __str__(self):
        return f'{self.name}'


class Photo(models.Model):
    description = models.TextField(verbose_name="Descriptions", blank=True, default=str)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name="Album", related_name="photo")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner", related_name="owner")
    photo = models.ImageField(upload_to="photo/")

    class Meta:
        verbose_name_plural = "Photos"

    def __str__(self):
        return f'User: {self.owner}, Description: {self.description}'

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.name))
        super().delete(*args, **kwargs)


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="Photo", related_name="comments")
    text = models.TextField(verbose_name="Text", blank=True, default=str)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner", related_name="comment")

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f'{self.owner}, {self.text}'


class Bookmark(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="Photo", related_name="bookmarks")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner", related_name="bookmarks")

    class Meta:
        verbose_name_plural = "Bookmarks"

    def __str__(self):
        return f'User: {self.owner}'
