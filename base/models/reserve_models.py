"""
予約モデルを定義
"""

from django.db import models
from django.contrib.auth import get_user_model
import datetime

def custom_timestamp_id():
    dt = datetime.datetime.now()
    return dt.strftime('%Y%m%d%H%M%S%f')

class Reserve(models.Model):
    id = models.CharField(default=custom_timestamp_id,
                        editable=False, primary_key=True, max_length=50)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザー')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name='店舗')

    # 予約日時
    reserved_time = models.DateTimeField(verbose_name='予約日時')
    
    # 予約人数
    number_of_people = models.PositiveSmallIntegerField(verbose_name='予約人数')

    # 作成・更新日時
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id