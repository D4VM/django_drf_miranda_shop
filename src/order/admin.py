from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'item_price',
        'quantity',
        'total_price',
        'completed',
        'created_at',
    )
