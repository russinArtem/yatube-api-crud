from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

v1_router = DefaultRouter()
v1_router.register(r'posts', PostViewSet, basename='posts')
v1_router.register(r'groups', GroupViewSet, basename='groups')

v1_comments_router = DefaultRouter()
v1_comments_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
] + v1_router.urls

urlpatterns += [
    path('posts/<int:post_id>/', include(v1_comments_router.urls)),
]

urlpatterns = [path('v1/', include(urlpatterns))]
