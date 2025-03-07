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

    
# class Store(models.Model):

#     GENRE_CHOICES = [
#         ('cafe', 'Cafe'),
#         ('restaurant', 'Restaurant'),
#         ('bar', 'Bar'),
#         ('shop', 'Shop'),
#         # 必要に応じて選択肢を追加
#     ]

#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     address = models.CharField(max_length=255)
#     hours = models.CharField(max_length=100)
#     website = models.URLField(blank=True, null=True)
#     image = models.ImageField(upload_to='stores/', blank=True, null=True)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
#     # genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)
    
#     genre = models.CharField(max_length=100, choices=GENRE_CHOICES, blank=True, null=True)
#     likes = models.PositiveIntegerField(default=0)  # いいねカウントの追加
#     # favorite_users = models.ManyToManyField(User, related_name='favorite_stores')

#     #QR
#     qr_code = models.ImageField(upload_to="qrcodes/", null=True, blank=True)  # 追加
#     unique_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
#     # unique_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
#     #\ unique_id = models.UUIDField(default=uuid.uuid4, unique=True)  # QRコード用の一意識別子

#     def generate_qr_code(store):
#         """
#         お店の詳細ページへ遷移するQRコードを生成
#         """
#         store_url = f"{settings.SITE_URL}store/{store.id}/"  # お店詳細ページのURL
#         qr = qrcode.make(store_url)

#         # 画像を保存
#         buffer = BytesIO()
#         qr.save(buffer, format="PNG")
#         filename = f"qr_codes/store_{store.id}.png"
        
#         store.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)

    
#     def save(self, *args, **kwargs):
#         if not self.id:  # ID が未設定の場合、最初に保存
#             super().save(*args, **kwargs)

#         if not self.qr_code:  # QRコードが未生成なら作成
#             self.generate_qr_code()
#             super().save(*args, **kwargs)  # 再度保存


#     def __str__(self):
#         return self.name

class Store(models.Model):

    GENRE_CHOICES = [
        ('cafe', 'Cafe'),
        ('restaurant', 'Restaurant'),
        ('bar', 'Bar'),
        ('shop', 'Shop'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    hours = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    
    qr_code = models.ImageField(upload_to="qrcodes/", null=True, blank=True)
    # unique_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)

    def generate_qr_code(self):
        """
        お店の詳細ページへ遷移するQRコードを生成
        """
        if not settings.SITE_URL:
            raise ValueError("SITE_URL is not defined in settings.")

        store_url = f"{settings.SITE_URL}store/{self.id}/"
        qr = qrcode.make(store_url)

        # 画像を保存
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        filename = f"qrcodes/store_{self.id}.png"

        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # 新規作成かどうかを確認
        super().save(*args, **kwargs)  # まず保存して ID を確定させる

        if is_new or not self.qr_code:  # 新規作成または QR コードが未生成の場合
            self.generate_qr_code()
            super().save(update_fields=["qr_code"])  # QRコードのみ更新

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

from django.utils import timezone
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    last_reset_date = models.DateField(default=timezone.now)  # 最後にポイントをリセットした日

    def reset_points_if_needed(self):
        """
        1ヶ月ごとにポイントをリセットする
        """
        today = timezone.now().date()
        if (today - self.last_reset_date).days >= 30:  # 30日経過していたらリセット
            self.points = 0
            self.last_reset_date = today
            self.save()
    def __str__(self):
        return f"{self.user.username} - {self.points} points"




class UserPointHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)  # いつポイントを獲得したか
    

    class Meta:
        unique_together = ('user', 'store')  # 同じ店舗のQRコードを2回スキャンできないようにする


from django.contrib.auth.models import User
from django.db import models

class UserPoint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def add_point(self, amount=1):
        self.points += amount
        self.save()
