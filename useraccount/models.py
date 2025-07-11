from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, UserManager, AbstractBaseUser
from cloudinary.models import CloudinaryField

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('you have to specify a valid email')
        email = self.normalize_email(email) 
        user = self.model(username=username, email=email,  **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    avatar = CloudinaryField(
        'avatar',
        folder='user_avatars',
        default='user_avatars/default.png',  # Set default image in Cloudinary
        transformation={'quality': 'auto:good'},
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    
    def get_username(self):
        return self.username
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        # Return default avatar URL if none exists
        return 'https://res.cloudinary.com/dia0j0tge/image/upload/v1749234171/default_afubcj.png'