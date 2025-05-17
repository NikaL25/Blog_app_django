from rest_framework import serializers
from .models import Blog, Comment, Notification

class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'photo', 'author', 'created_at', 'updated_at', 'like_count']
        extra_kwargs = {
            'title': {'help_text': 'Blog title (up to 200 characters).'},
            'description': {'help_text': 'Blog description.'},
            'photo': {'help_text': 'Blog image (optional).'},
            'author': {'help_text': 'Blog author name (read-only).'},
            'like_count': {'help_text': 'Number of likes (read-only).'},
        }

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    blog_id = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), source='blog')
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), source='parent', allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'blog_id', 'author', 'text', 'created_at', 'parent_id']
        extra_kwargs = {
            'text': {'help_text': 'Comment text.'},
            'blog_id': {'help_text': 'ID of the blog the comment belongs to.'},
            'parent_id': {'help_text': 'ID of the parent comment (for replies, optional).'},
        }

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_type', 'target_id', 'created_at', 'is_read']
        extra_kwargs = {
            'verb': {'help_text': 'The action (e.g. "liked", "commented").'},
            'target_type': {'help_text': 'The target type ("blog" or "comment").'},
            'target_id': {'help_text': 'The target ID (blog or comment).'},
            'is_read': {'help_text': 'Whether the notification has been read.'},
         }