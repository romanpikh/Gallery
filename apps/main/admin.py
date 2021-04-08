from django.contrib import admin

# Register your models here.
from .models import Photo, Album, Comment, Bookmark


class PhotoInlines(admin.TabularInline):
    model = Photo
    extra = 0


class CommentInlines(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInlines]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    inlines = [CommentInlines]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass
