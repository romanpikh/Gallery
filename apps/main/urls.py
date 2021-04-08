from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.main.views import AlbumViewSet, PhotoViewSet, CommentViewSet, BookmarkViewSet, DeleteBookmarkViewSet, \
    DeleteCommentViewSet, PhotoUpdateViewSet, AllPhotoViewSet

urlpatterns = [
    path('albums/', AlbumViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('albums/<int:pk>/delete/', AlbumViewSet.as_view({'get': 'list', 'delete': 'destroy'})),

    path('photos/', PhotoViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('photos/<int:pk>/', PhotoViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('photos/<int:photo_id>/comments/', CommentViewSet.as_view({'post': 'create'})),
    path('photos/<int:photo_pk>/comments/<int:pk>/', DeleteCommentViewSet.as_view({'delete': 'destroy'})),

    path('users/<int:pk>/update/', PhotoUpdateViewSet.as_view({'get': 'retrieve', 'put': 'update'})),

    path('bookmarks/<int:photo_id>/create/', BookmarkViewSet.as_view()),
    path('bookmarks/<int:pk>/delete/', DeleteBookmarkViewSet.as_view()),

    path('feed/',  AllPhotoViewSet.as_view({'get': 'list'})),
]
