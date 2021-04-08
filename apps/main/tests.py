from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.main.models import Album, User, Photo, Comment, Bookmark


class ModelsTestCase(TestCase):

    def test_album(self):
        """ correctly Album when saving """

        self.user = User.objects.create_user(username='testuser', password='1231111', email='email@email.com')
        album = Album.objects.create(name="My first album", owner=self.user)
        album.save()
        self.assertEqual(album.name, "My first album")

    def test_photo(self):
        """ correctly Photo when saving """

        description = "description text and another text124 $@@%$#% "
        photo = "wwwedfsfsf.jpg"
        self.user = User.objects.create_user(username='testuser', password='1231111', email='email@email.com')
        self.album = Album.objects.create(name="My first album", owner=self.user)

        photos = Photo.objects.create(description=description, owner=self.user, photo=photo, album=self.album)
        photos.save()
        self.assertEqual(photos.description, description)
        self.assertEqual(photos.photo.name, photo)

    def test_comment(self):
        """ correctly Comment when saving """

        description = "description text and another text124 $@@%$#% "
        photo = "wwwedfsfsf.jpg"
        user = User.objects.create_user(username='testuser', password='1231111', email='email@email.com')
        album = Album.objects.create(name="My first album", owner=user)

        photos = Photo.objects.create(description=description, owner=user, photo=photo, album=album)
        comment = Comment.objects.create(owner=user, photo=photos, text=description)
        comment.save()
        self.assertEqual(comment.text, description)
        self.assertEqual(comment.photo.photo, photo)
        self.assertEqual(comment.owner, user)

    def test_bookmark(self):
        """ correctly Bookmark when saving """

        description = "description text and another text124 $@@%$#% "
        photo = "wwwedfsfsf.jpg"
        user = User.objects.create_user(username='testuser', password='1231111', email='email@email.com')
        album = Album.objects.create(name="My first album", owner=user)
        photos = Photo.objects.create(description=description, owner=user, photo=photo, album=album)

        bookmark = Bookmark.objects.create(owner=user, photo=photos)
        bookmark.save()
        self.assertEqual(bookmark.owner, user)
        self.assertEqual(bookmark.photo, photos)


class RegistrationTest(TestCase):

    def test_registration(self):
        data = {"username": "test_name", "email": "email@mail.app", "password1": "pass_strong",
                "password2": "pass_strong", "first_name": "my_name", "last_name": "my_last_name"}
        response = self.client.post("/api/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
