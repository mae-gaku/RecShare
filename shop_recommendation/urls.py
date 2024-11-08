# shop_recommendation/urls.py
from django.contrib import admin
from django.urls import path
from stores import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # メインページをルートURLに設定
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('store/<int:store_id>/qr/', views.generate_qr_code, name='generate_qr_code'),
    path('store/', views.store_list, name='store_list'),
    path('store_group_list/<int:group_id>/', views.store_group_list, name='store_group_list'),
    path('register_store/', views.register_store, name='register_store'),
    # path('register_dish/', views.register_dish, name='register_dish'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('signup/', views.signup, name='signup'),
    # path('register/register_store_with_dishes/', views.register_store_with_dishes, name='register_store_with_dishes'),
]


from django.conf import settings
from django.conf.urls.static import static


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

