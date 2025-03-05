# Generated by Django 5.1.6 on 2025-03-05 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierProfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(help_text='The month for the profit', verbose_name='Month')),
                ('profit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.supplier')),
            ],
            options={
                'unique_together': {('supplier', 'month')},
            },
        ),
    ]
