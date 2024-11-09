from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    # Get all the users that the current user is following
    following_users = request.user.following.all()
    # Get posts from these followed users, ordered by creation date
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serialized_posts = PostSerializer(posts, many=True)
    
    return Response(serialized_posts.data)


@login_required
def like_post(request, pk):
    # Get the post or return 404 if not found
    post = get_object_or_404(Post, pk=pk)
    
    # Create or get the Like object
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if created:
        # If a like was created, generate a notification for the post's author
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post,
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.pk
        )
    
    # Redirect the user back to the post detail view (or wherever necessary)
    return redirect('post_detail', pk=pk)

@login_required
def unlike_post(request, pk):
    # Get the post or return 404 if not found
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the user has already liked the post, if so, delete the like
    like = Like.objects.filter(user=request.user, post=post).first()
    
    if like:
        like.delete()  # Delete the like if it exists
    
    # Redirect the user back to the post detail view (or wherever necessary)
    return redirect('post_detail', pk=pk)


# "generics.get_object_or_404(Post, pk=pk)" ?