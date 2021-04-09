from django.core.handlers import exception
from django.db.models import Max, Sum, F, Count
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.main.models import Album, Photo, Comment, Bookmark
from apps.main.serializer import AlbumSerializer, PhotoSerializer, CommentSerializer, BookmarkSerializer, \
    ShortPhotoSerializer, PhotoListSerializer, CreatePhotoSerializer, DetailPhotoSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(owner=self.request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Album, owner=self.request.user, pk=self.kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = CreatePhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsAuthenticated]


class PhotoUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = ShortPhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Photo, pk=self.kwargs["pk"], owner=self.request.user)
        serializer = DetailPhotoSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(Photo, pk=self.kwargs["pk"], owner=self.request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
        Create comment to photo
    """
    lookup_field = "photo_id"
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        photo = get_object_or_404(Photo, pk=self.kwargs["photo_id"])
        Comment.objects.create(owner=self.request.user, photo=photo, text=serializer.data["text"])


class DeleteCommentViewSet(viewsets.ModelViewSet):
    """
        Delete comment from photo
    """
    lookup_field = "photo_pk"
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(owner=self.request.user, id=self.kwargs["photo_pk"]))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, owner=self.request.user, pk=self.kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookmarkViewSet(generics.CreateAPIView):
    """
        Create Bookmarks
    """
    lookup_field = "photo_id"
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
    permission_classes = [IsAuthenticated]


class DeleteBookmarkViewSet(generics.DestroyAPIView):
    """
        Delete  bookmarks
    """
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
    permission_classes = [IsAuthenticated]


class AllPhotoViewSet(viewsets.ReadOnlyModelViewSet):
    """
        All photos are sorted in descending order of the number of comments and likes
    """
    queryset = Photo.objects.all().annotate(comm=Count("comments"), book=Count("bookmarks"),
                                            count=F("comm") + F("book")).order_by("-count")
    serializer_class = PhotoListSerializer
    permission_classes = [AllowAny]
