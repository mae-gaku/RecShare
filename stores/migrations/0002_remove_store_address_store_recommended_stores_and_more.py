# Generated by Django 4.0.6 on 2024-08-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='address',
        ),
        migrations.AddField(
            model_name='store',
            name='recommended_stores',
            field=models.ManyToManyField(blank=True, related_name='recommended_by', to='stores.store'),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='store',
            name='website',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='StoreGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stores', models.ManyToManyField(related_name='groups', to='stores.store')),
            ],
        ),
    ]
