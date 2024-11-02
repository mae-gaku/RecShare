from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    
class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    hours = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # genres = models.ManyToManyField(Genre)  # 多対多の関係でジャンルを紐づけ
    # genre = models.CharField(max_length=50)  # ジャンルフィールドを追加
    # genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class StoreGroup(models.Model):
    name = models.CharField(max_length=255)
    stores = models.ManyToManyField('Store', related_name='store_groups')

    def __str__(self):
        return self.name


class Review(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーシステムがある場合
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)  # 1から5の評価
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.store.name}のレビュー by {self.user.username}'
