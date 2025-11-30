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

urlpatterns = [
    path('admin/', admin.site.urls),

    # トップページ
    path('', views.IndexListView.as_view(), name='index'),

    # 店舗一覧
    path('restaurants/', views.ShopListView.as_view(), name="restaurants"),

    # 店舗詳細
    path('restaurants/<int:pk>/', views.ShopDetailView.as_view(), name="detail"),

    # Account
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),          # ただログアウトさせるだけなのでDjangoの標準機能を実装し、viewsの指定はなし
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('account/', views.AccountUpdateView.as_view(),name='account'),

]
