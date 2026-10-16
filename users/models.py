"""
Модели приложения users.Определяет кастомную модель пользователя, контакты (адреса доставки)
и токены подтверждения email.
User — кастомный пользователь с ролями 'buyer' / 'shop'.
Contact — адреса доставки, привязанные к пользователю.
ConfirmEmailToken — токены для подтверждения email при регистрации.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid



class User(AbstractUser):
    
    USER_TYPE = [('buyer', 'Покупатель'), ('shop', 'Магазин'),]

    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    company = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=10, choices=USER_TYPE, default='buyer', verbose_name='Тип пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return f'{self.username} ({self.email})'


class Contact(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом')
    apartment = models.CharField(max_length=15, blank=True, verbose_name='Квартира')
    phone = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['id']

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house}, {self.phone}'


class ConfirmEmailToken(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirm_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_token(cls, user):
        token = uuid.uuid4().hex
        obj = cls.objects.create(user=user, token=token)
        return obj

    class Meta:
        verbose_name = 'Токен подтверждения'
        verbose_name_plural = 'Токены подтверждения'

    def __str__(self):
        return f'{self.user.email} — {self.token[:8]}...'



