# Generated by Django 5.0.4 on 2024-05-15 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_featured_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='featured_image',
        ),
    ]
