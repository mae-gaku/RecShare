# Generated by Django 4.0.6 on 2024-10-27 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_store_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='genres',
        ),
        migrations.AddField(
            model_name='store',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stores.genre'),
        ),
    ]
