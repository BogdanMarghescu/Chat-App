from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, username, password=None):
        """Create a new user profile"""
        if not username:
            raise ValueError("You must provide an username")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """Create a new superuser"""
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    object = UserProfileManager()
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def get_username(self):
        """"Retrieve username"""
        return self.username

    def __str__(self):
        """Return string representation of our user"""
        return self.username
