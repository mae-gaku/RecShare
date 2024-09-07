from django.db import models
from django.urls import reverse


class Store(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    recommended_stores = models.ManyToManyField('self', blank=True, related_name='recommended_by')
    image = models.ImageField(upload_to='store_images/', blank=True, null=True)  # 画像フィールドを追加
    
    def __str__(self):
        return self.name
    
class Dish(models.Model):
    store = models.ForeignKey(Store, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 料理の価格を追加

    def __str__(self):
        return self.name
    
# class QRCode(models.Model):
#     store = models.OneToOneField(Store, on_delete=models.CASCADE)
#     code = models.ImageField(upload_to='qrcodes/')

#     def __str__(self):
#         return f"QR Code for {self.store.name}"


class StoreGroup(models.Model):
    name = models.CharField(max_length=255)
    stores = models.ManyToManyField('Store', related_name='store_groups')

    def __str__(self):
        return self.name





