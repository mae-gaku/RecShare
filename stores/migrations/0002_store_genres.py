# Generated by Django 4.0.6 on 2024-10-27 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='genres',
            field=models.ManyToManyField(to='stores.genre'),
        ),
    ]