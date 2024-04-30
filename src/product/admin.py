from django.contrib import admin

from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    fields = (
        'title',
        'category',
        'child_category',
        'product_style',
        'barcode',
        'stock',
        'price',
        'discount',
        'size',
        'color',

    )