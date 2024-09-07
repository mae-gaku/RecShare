# Generated by Django 4.0.6 on 2024-08-16 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_store_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='dishes/')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='stores.store')),
            ],
        ),
    ]