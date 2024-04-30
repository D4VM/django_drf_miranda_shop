from django.db import models
from product.models import Product
from user.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product")
    quantity = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.product.title

    def total_price(self):
        return self.quantity * self.product.get_sale_price()

    def item_price(self):
        return self.product.get_sale_price()

