from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Blog, Comment, Notification
from .serializers import BlogSerializer, CommentSerializer, NotificationSerializer
from django.contrib.auth.models import User
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['author', 'title']
    ordering_fields = ['created_at', 'like_count']
    
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={201: BlogSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={200: openapi.Response('Blog liked'), 400: openapi.Response('Error')}
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        blog = self.get_object()
        if blog.author != request.user:
            blog.like_count += 1
            blog.save()
            Notification.objects.create(
                recipient=blog.author,
                sender=request.user,
                message=f"{request.user.username} liked your blog: {blog.title}"
            )
            return Response({'status': 'blog liked'}, status=status.HTTP_200_OK)
        return Response({'error': 'Cannot like own blog'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blog_id', 'parent_id']
    
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={201: CommentSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        blog = serializer.validated_data['blog_id']
        if blog.author != self.request.user:
            Notification.objects.create(
                recipient=blog.author,
                sender=self.request.user,
                message=f"{self.request.user.username} commented on your blog: {blog.title}"
            )

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        if not self.request.user.is_authenticated:
            return Notification.objects.none()
        return Notification.objects.filter(recipient=self.request.user)
    
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        responses={200: openapi.Response('Notification marked as read')}
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'}, status=status.HTTP_200_OK)