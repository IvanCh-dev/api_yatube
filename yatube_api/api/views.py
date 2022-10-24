from rest_framework import viewsets
from posts.models import Group, Post, Comment
from rest_framework.permissions import IsAuthenticated
from django.core import exceptions
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrAdmin


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Админу запрещено редактировать чужие записи."""
        author = Post.objects.get(id=self.kwargs.get('pk')).author
        if self.request.user != author:
            raise exceptions.PermissionDenied(
                'Админ, чужие записи можешь только удалять.')
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, ]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin, ]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post=post_id)
        return queryset

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """Админу запрещено редактировать чужие записи."""
        author = Comment.objects.get(id=self.kwargs.get('pk')).author
        if self.request.user != author:
            raise exceptions.PermissionDenied(
                'Админ, чужие записи можешь только удалять.')
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_destroy(self, instance):
        instance.delete()
