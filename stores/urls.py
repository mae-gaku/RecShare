# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('stores/', views.store_list, name='store_list'),
#     path('store/<int:store_id>/', views.store_detail, name='store_detail'),
#     path('store/<int:store_id>/recommendations/', views.recommendations, name='recommendations'),
#     path('store/<int:store_id>/qr/', views.generate_qr_code, name='generate_qr_code'),  # これを追加
#     path('store_group_list/<int:group_id>/', views.store_group_list, name='store_group_list'),
# ]

# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('stores/', views.store_list, name='store_list'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('store/<int:store_id>/recommendations/', views.recommendations, name='recommendations'),
    path('store/<int:store_id>/qr/', views.generate_qr_code, name='generate_qr_code'),
    path('store_group_list/<int:group_id>/', views.store_group_list, name='store_group_list'),
    path('register_store/', views.register_store, name='register_store'),
    path('register_dish/', views.register_dish, name='register_dish'),
    # path('register_store_with_dishes/', views.register_store_with_dishes, name='register_store_with_dishes'),
]
