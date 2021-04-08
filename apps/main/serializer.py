from rest_framework import serializers

from apps.main.models import Album, Photo, Comment, Bookmark


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(owner=self.context['request'].user)
        return super().to_representation(data)


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ["id", "owner", "name"]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = Comment
        fields = ["pk", "text"]


class CreatePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ["id", "owner", "photo", "album", "description"]


class PhotoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Photo
        fields = ["id", "owner", "photo", "album", "description", "comments"]


class DetailPhotoSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Photo
        fields = ["id", "owner", "photo", "album", "description"]


class ShortPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ["description"]


class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ["photo", "owner"]


class PhotoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ["id", "owner", "photo", "album", "description"]
