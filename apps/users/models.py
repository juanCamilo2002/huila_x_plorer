from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from core.models import BaseModel

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(unique=True)
    objects = UserManager()


    ROLE_CHOICES = (
        ('USER', 'Mobile User'),
        ('ADMIN', 'Admin')
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    phone = models.CharField(max_length=20, blank=True, null=True)

    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()