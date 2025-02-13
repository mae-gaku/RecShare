from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import os
import qrcode
from django.conf import settings

import uuid
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    
class Store(models.Model):

    GENRE_CHOICES = [
        ('cafe', 'Cafe'),
        ('restaurant', 'Restaurant'),
        ('bar', 'Bar'),
        ('shop', 'Shop'),
        # 必要に応じて選択肢を追加
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    hours = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)
    
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)  # いいねカウントの追加
    favorite_users = models.ManyToManyField(User, related_name='favorite_stores')

    #QR
    qr_code = models.ImageField(upload_to="qrcodes/", null=True, blank=True)  # 追加
    unique_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    # unique_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    #\ unique_id = models.UUIDField(default=uuid.uuid4, unique=True)  # QRコード用の一意識別子

    def generate_qr_code(self):
        """ QRコードを生成し、画像として保存 """
        qr = qrcode.make(f"https://example.com/scan/?store_id={self.unique_id}")
        qr_io = BytesIO()
        qr.save(qr_io, format='PNG')
        self.qr_code.save(f'qr_{self.unique_id}.png', ContentFile(qr_io.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'store')  # ユーザーと店舗の組み合わせを一意に制限


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


from django.db import models
from django.contrib.auth.models import User

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.store.name} ({self.interaction_type})"


class ViewLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.store.name} at {self.viewed_at}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"




class UserPointHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)  # いつポイントを獲得したか

    class Meta:
        unique_together = ('user', 'store')  # 同じ店舗のQRコードを2回スキャンできないようにする
