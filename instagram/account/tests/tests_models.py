# Python standard library
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Type

# Django imports
from django.test import TestCase
from django.db.models import Model
from django.db.models import QuerySet

# Instagram models
from instagram.account.models import User
from instagram.account.models import Profile


class BaseTestCase(TestCase):

    def setUp(self) -> None:
        self.user: Type['User'] = User.objects.create_user(
            first_name='User',
            last_name='Test',
            username='testuser',
            email='usertest@example.com',
            password='!([p@SS-+w0rd)001}'
        )

    def get_queryset(self, klass: Model, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        if args or kwargs:
            return klass.objects.filter(*args, **kwargs).first()

        return klass.objects.all()


class AccountModelsTestCase(BaseTestCase):

    def test_user_data(self) -> None:
        user = self.get_queryset(User, username='testuser')

        self.assertEquals(user.username, 'testuser')
        self.assertEquals(user.email, 'usertest@example.com')
        self.assertAlmostEqual(user.get_full_name(), 'User Test')

    def test_user_permissions(self) -> None:
        user = self.get_queryset(User, email='usertest@example.com')

        self.assertEquals(user.is_superuser, False)
        self.assertEquals(user.is_staff, False)
        self.assertEquals(user.is_active, True)
        self.assertEquals(user.is_verified, False)

    def test_update_user_data(self) -> None:
        user = self.get_queryset(User, username='testuser')

        self.assertEquals(user.username, 'testuser')
        user.username = 'supertestuser'
        user.first_name = 'Another'
        user.last_name = 'Example'
        user.email = 'another_test@example.com'
        user.save()
        self.assertEquals(user.username, 'supertestuser')
        self.assertEquals(user.first_name, 'Another')
        self.assertEquals(user.last_name, 'Example')
        self.assertEquals(user.email, 'another_test@example.com')
        self.assertEquals(user.get_full_name(), 'Another Example')

    def test_profile_model(self) -> None:
        user = self.get_queryset(User, username='testuser')
        profile = Profile.objects.filter(user__username=user).first()

        self.assertEquals(user, profile.user)
        self.assertEquals(user.username, profile.user.username)