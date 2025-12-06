"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from base.views import reserve_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # トップページ
    path('', views.IndexListView.as_view(), name='index'),

    # 店舗一覧
    path('restaurants/', views.ShopListView.as_view(), name="restaurants_list"),

    # 店舗詳細
    path('restaurants/<int:pk>/', views.ShopDetailView.as_view(), name="restaurants_detail"),

    # Account
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),          # ただログアウトさせるだけなのでDjangoの標準機能を実装し、viewsの指定はなし
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('mypage/account/', views.AccountDetailView.as_view(), name='account_detail'),
    path('mypage/account/edit/', views.AccountUpdateView.as_view(), name='account_edit'),

    # favorite
    path('mypage/favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('mypage/favorites/<int:pk>/', views.FavoriteToggleView.as_view(), name='favorites_toggle01'),
    path('mypage/favorites/<int:pk>#favarite', views.FavoriteToggleView.as_view(), name='favorites_toggle02'),
    path('mypage/favorites/<int:pk>/delete/', views.FavoriteToggleView.as_view(), name='favorites_delete'),

    # review
    path('restaurants/<int:pk>/reviews/', views.ShopReviewView.as_view(), name='reviews'),
    path('restaurants/<int:pk>/reviews/create/', views.ShopReviewCreateView.as_view(), name='review_create'),
    path('restaurants/<int:shop_pk>/reviews/<int:review_pk>/delete/', views.ShopReviewDeleteView.as_view(), name='review_delete'),

    # reserve
    path('restaurants/<int:pk>/reserve/', views.ReserveCreateView.as_view(), name='reserve'),
    path('mypage/reservations/', views.ReserveListView.as_view(), name='reserve_list'),
    path('reserve/<str:pk>/delete/', views.ReserveDeleteView.as_view(), name='reserve_delete'),

]

# 画像の設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)