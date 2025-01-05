from django.contrib import admin
from .models import Store
from .models import StoreGroup
from django.contrib import admin
# from .models import Store, Dish, Review
from .models import Store, Review, Genre, ViewLog
admin.site.register(Store)
# admin.site.register(QRCode)
admin.site.register(StoreGroup)
admin.site.register(Genre)
admin.site.register(ViewLog)

class StoreAdmin(admin.ModelAdmin):
    # inlines = [DishInline]
    list_display = ('name', 'description')
    filter_horizontal = ('recommended_stores',)  # ManyToManyField 用の UI を提供

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('store', 'user', 'rating', 'created_at')
