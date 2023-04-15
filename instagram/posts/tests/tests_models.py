# Python standard library
from typing import Any
from typing import Dict
from typing import Tuple

# Django imports
from django.test import TestCase
from django.db.models import Model
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

# Instagram models
from instagram.account.models import User
from instagram.posts.models import Post
from instagram.posts.models import Comment
from instagram.posts.models import Like


class BaseTestCase(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            first_name='User',
            last_name='Test',
            username='usertest',
            email='email@example.com',
            password='password12345678'
        )
        self.post = Post.objects.create(
            author=self.user,
            image='test_image.png',
            thumbnail='test_image_thumbnail.png',
            description='Hello world'
        )
    
    def get_queryset(self, klass: Model, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        if args or kwargs:
            return klass.objects.filter(*args, **kwargs).first()
        
        return klass.objects.all()


class PostModelTestCase(BaseTestCase):
    
    def test_post_data(self) -> None:
        user = self.get_queryset(get_user_model(), username='usertest')
        post = self.get_queryset(Post, author__username=user.username)
        posts = self.get_queryset(Post)

        self.assertEquals(post.image, 'test_image.png')
        self.assertEquals(post.thumbnail, 'test_image_thumbnail.png')
        self.assertEquals(post.description, 'Hello world')
        self.assertEquals(posts.count(), 1)
    
    def test_update_post(self) -> None:
        post = self.get_queryset(Post, pk=1)
        
        post.description = 'Updated description'
        self.assertNotEquals(post.description, 'Hello world')
        self.assertEquals(post.description, 'Updated description')
    
    def test_post_author_data(self) -> None:
        user = self.get_queryset(User, username='usertest')
        post = self.get_queryset(Post, pk=1)
        
        self.assertEquals(post.author, user)
        self.assertEquals(post.author.username, 'usertest')
        self.assertEquals(post.author.first_name, user.first_name)


class CommentModelTestCase(BaseTestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self.comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            body='Nice picture'
            
        )
    
    def test_comment_data(self) -> None:
        user = self.get_queryset(get_user_model(), email='email@example.com')
        post = self.get_queryset(Post, author__username=user.username)
        comment = self.get_queryset(Comment, pk=1)
        
        self.assertEquals(comment.author, user)
        self.assertEquals(comment.post, post)
        self.assertEquals(comment.body, 'Nice picture')
    
    def test_comment_update(self) -> None:
        user = self.get_queryset(User, username='usertest')
        comment = self.get_queryset(Comment, author__username=user.username)
        
        comment.body = 'Changed comment'
        self.assertEquals(comment.body, 'Changed comment')
        self.assertNotEquals(comment.body, 'Nice picture')
    
    def test_comment_user_data(self) -> None:
        user = self.get_queryset(get_user_model(), username='usertest')
        comment = self.get_queryset(Comment, pk=1)
        
        self.assertEquals(comment.author, user)
        self.assertEquals(comment.author.first_name, 'User')
        self.assertEquals(comment.author.last_name, 'Test')
        self.assertNotEquals(comment.author.username, 'Simon')


class LikeModelTestCase(BaseTestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self.like = Like.objects.create(user=self.user, post=self.post)
    
    def test_count_likes(self) -> None:
        post = self.get_queryset(Post, pk=1)
        likes = self.get_queryset(Like)
        
        self.assertEquals(post.total_likes, 1)
        self.assertEquals(likes.count(), 1)
    
    def test_like_user_data(self) -> None:
        user = self.get_queryset(User, username='usertest')
        like = self.get_queryset(Like, pk=1)
        
        self.assertEquals(like.user, user)
        self.assertEquals(like.user.username, user.username)
        self.assertNotEquals(like.user.first_name, 'Rails')
    
    def test_like_post_data(self) -> None:
        user = self.get_queryset(User, username='usertest')
        post = self.get_queryset(Post, author__username=user.username)
        like = self.get_queryset(Like, pk=1)
        
        self.assertEquals(like.post, post)
        self.assertEquals(like.post.description, post.description)
        self.assertEquals(like.post.image.name, 'test_image.png')