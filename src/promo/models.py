from django.db import models

from product.models import Product


class Promo(models.Model):
    title = models.CharField(max_length=250)
    featured_image = models.ImageField(upload_to="promo")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title
