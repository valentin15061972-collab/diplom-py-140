from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid



class User(AbstractUser):
    
    USER_TYPE = [('buyer', 'Покупатель'), ('shop', 'Магазин'),]

    email = models.EmailField(unique=True)
    company = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=10, choices=USER_TYPE, default='buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.username} ({self.email})'


class Contact(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.address}, {self.phone}'


class ConfirmEmailToken(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirm_tokens')
    token = models.CharField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_token(cls, user):
        token = uuid.uuid4().hex
        obj = cls.objects.create(user=user, token=token)
        return obj

    def __str__(self):
        return f'{self.user.email} — {self.token[:8]}...'



