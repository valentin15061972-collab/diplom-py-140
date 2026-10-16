from django.db import models
from django.core.validators import MinValueValidator
from users.models import User, Contact
from products.models import ProductInfo, Shop
"""
Модели приложения orders.
Определяет модели заказов и позиций заказа.
Заказ привязан к пользователю, контакту (адресу доставки)
и содержит набор позиций, каждая из которых ссылается
на товар конкретного магазина.

Order — заказ пользователя со статусом и адресом доставки.
OrderItem — позиция заказа (товар, магазин, количество).
"""

class Order(models.Model):
    
    STATUS_CHOICES = [('created', 'создан'), ('confirmed', 'подтверждён'), ('sent', 'отправлен'), 
                      ('delivered', 'доставлен'), ('canceled', 'отменён')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders', verbose_name='Адрес доставки')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} — {self.user.email} — {self.status}'

    @property
    def total_sum(self):
        return sum(item.total_cost for item in self.items.all())

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def confirm(self, contact):
        self.status = 'confirmed'
        self.contact = contact
        self.save()


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='order_items', verbose_name='Информация о товаре')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='order_shops', verbose_name='Магазин')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        ordering = ['id']

    def __str__(self):
        return f'{self.product_info.product.name} x {self.quantity}'

    @property
    def total_cost(self):
        return self.product_info.price * self.quantity
