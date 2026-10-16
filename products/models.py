"""
Модели приложения products.
Определяет модель магазина, категории, товары, информацию о ценах
и остатках, а также настраиваемые характеристики товаров.
Shop — информация о магазине и его владельце.
Category — категории товаров.
Product — базовая информация о товаре.
ProductInfo — цена и количество товара в конкретном магазине.
Parameter — настраиваемая характеристика товара.
ProductParameter — значение характеристики для товара в магазине.
"""

from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Shop(models.Model):

    name = models.CharField(max_length=50, blank=True, verbose_name='Название')
    url = models.URLField(blank=True, verbose_name='Ссылка')
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='shop', verbose_name='Владелец')
    state = models.BooleanField(default=True, verbose_name='Статус заказа')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=50, verbose_name='Название')
    shops = models.ManyToManyField(Shop, related_name='categories', blank=True, verbose_name='Магазины')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='products', verbose_name='Категория')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def shops_with_product(self):
        return list(Shop.objects.filter(product_info__product=self).distinct())


class ProductInfo(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_info', verbose_name='Товар')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='product_info', verbose_name='Магазин')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Цена')
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Розничная цена')

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'
        ordering = ['id']

    def __str__(self):
        return f'{self.product.name} — {self.shop.name} — {self.price}'

    @property
    def total_cost(self):
        return self.price * self.quantity


class Parameter(models.Model):

    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductParameter(models.Model):

    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='parameters', verbose_name='Информация о товаре')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='product_parameters', verbose_name='Параметр')
    value = models.CharField(max_length=100, verbose_name='Значение')

    class Meta:
        verbose_name = 'Параметр товара'
        verbose_name_plural = 'Параметры товаров'
        ordering = ['id']

    def __str__(self):
        return f'{self.parameter.name}: {self.value}'
