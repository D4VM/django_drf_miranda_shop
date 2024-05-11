# Generated by Django 5.0.4 on 2024-05-08 07:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promo',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='promo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]