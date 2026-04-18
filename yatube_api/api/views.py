from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, instance):
        return (
            request.method in permissions.SAFE_METHODS
            or instance.author == request.user
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)
