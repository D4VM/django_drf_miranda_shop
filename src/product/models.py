from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=250, blank=True, null=True)
    child_category = models.CharField(max_length=250, blank=True, null=True)
    product_style = models.CharField(max_length=250, blank=True, null=True)
    barcode = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)

    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_sale_price(self) -> float:
        if not self.discount:
            return self.price
        return round(self.price - (self.price * self.discount) / 100, 2)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)


