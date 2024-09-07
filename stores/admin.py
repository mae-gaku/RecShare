from django.contrib import admin
from .models import Store
from .models import StoreGroup
admin.site.register(Store)
# admin.site.register(QRCode)
admin.site.register(StoreGroup)

from django.contrib import admin
from .models import Store, Dish

class DishInline(admin.TabularInline):
    model = Dish
    extra = 1

class StoreAdmin(admin.ModelAdmin):
    inlines = [DishInline]

admin.site.register(Dish)
