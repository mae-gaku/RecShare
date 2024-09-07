# Generated by Django 4.0.6 on 2024-09-07 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0006_dish'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
