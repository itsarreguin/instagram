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
        Post.objects.create(
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