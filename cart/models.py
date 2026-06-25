from django.db import models

# Create your models here.

class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """
    Элемент корзины конкретного пользователя.
    Хранит товар, выбранный цвет и память, количество и цену.
    """
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ('cart', 'product')  # один товар+вариант памяти+цвет один раз

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    # def total_price(self):
    #     return self.price * self.quantity

