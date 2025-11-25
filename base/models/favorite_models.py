"""
予約モデルを定義
"""

from django.db import models
from django.contrib.auth import get_user_model

class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザー')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name='店舗')

    class Meta:
        unique_together = ('user', 'shop')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} (登録店舗：{self.shop.name})"
