"""
レビューモデルを定義
"""
from django.db import models
from django.contrib.auth import get_user_model

class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name='レビューユーザー')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name='レビュー店舗')

    # 評価
    score = models.SmallIntegerField(verbose_name='評価点', choices=[(i, i) for i in range(1, 6)]) # 1～5で評価
    
    # 内容
    content = models.TextField(default='', blank=True, verbose_name='レビュー内容')

    # 作成・更新日時
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} (店舗名：{self.shop.name} / {self.score}点)"