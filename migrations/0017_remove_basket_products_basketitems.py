# Generated by Django 5.1 on 2024-09-27 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0016_basket_products_delete_basketitems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='products',
        ),
        migrations.CreateModel(
            name='BasketItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shopping.basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.product')),
            ],
            options={
                'unique_together': {('basket', 'product')},
            },
        ),
    ]
