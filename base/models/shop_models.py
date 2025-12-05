"""
店舗モデルを定義
"""
from django.db import models
from django.utils.crypto import get_random_string
import os

def create_id():
    return get_random_string(22)

"""
修正予定：vegeketで画像処理失敗したため調整必要？
"""
def upload_image_to(instance, filename):
    return f'{instance.id}/{filename}'


"""
カテゴリー
"""
class Category(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='カテゴリー名')
    slug = models.CharField(max_length=32, unique=True, verbose_name='スラッグ') 
    def __str__(self):
        return self.name
    
    """
    検索結果にて使用検討
    def total(self):
        return Shop.objects.filter(category=self.id).count()
    """

"""
タグ
"""
class Tag(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='タグ名')
    slug = models.CharField(max_length=32, unique=True, verbose_name='スラッグ') 
    def __str__(self):
        return self.name
    
"""
定休日の設定
"""
# 曜日マスタ
class Weekday(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='管理コード')
    name = models.CharField(max_length=10, unique=True, verbose_name='曜日')

# 店舗と曜日を紐づける定休日モデル
class Regular_holidays(models.Model):
    id = models.AutoField(primary_key=True)
    shop = models.ForeignKey('Shop', on_delete=models. CASCADE,related_name='regular_holidays_relationship')
    weekday = models.ForeignKey('Weekday', on_delete=models.CASCADE)
    # 実際定休日かどうかを店舗ごとに設定
    is_holiday = models.BooleanField(default=False, verbose_name='定休日設定')
    # DBに同じ店舗-曜日の組み合わせがないようにする
    class Meta:
        unique_together = ('shop', 'weekday')

    def __str__(self):
        return self.name

"""
店舗情報
"""
class Shop(models.Model):   # Modelは、jangoのクラスで継承している
    # id = models.CharField(default=create_id, primary_key=True, max_length=50, editable=False)
    name = models.CharField(max_length=50, verbose_name='店名')
    mail = models.CharField(default='', blank=True, max_length=255, verbose_name='メールアドレス')
    zipcode = models.CharField(default='', blank=True, max_length=8, verbose_name='郵便番号')
    address = models.CharField(default='', blank=True, max_length=255, verbose_name='住所')
    tel = models.CharField(default='', blank=True, max_length=15, verbose_name='電話番号')
    description = models.TextField(default='', blank=True, verbose_name='説明')
    price = models.CharField(default='', blank=True, max_length=50, verbose_name='平均予算')
    seating_capacity = models.TextField(default='', blank=True, verbose_name='席数')
    opening_hours = models.TextField(default='', blank=True, verbose_name='営業時間・ラストオーダーの案内')
    holiday = models.TextField(default='', blank=True, verbose_name='定休日の案内')
    reserve_start_time = models.TimeField(default=None, blank=True, verbose_name='予約開始時間')
    reserve_end_time = models.TimeField(default=None, blank=True, verbose_name='予約終了時間')

    # 画像
    image = models.ImageField(default='noImage.png', blank=True, upload_to=upload_image_to,  verbose_name='画像')
    # image = models.ImageField(default='noImage.png', blank=True,  verbose_name='画像')


    # カテゴリー # ForeignKeyとon_delete=はセットで必須
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)    
    # タグ（中間フィールド）
    # 複数設定することを前提にtagsとし、ManyToManyFieldで定義することで中間フィールドとする
    tags = models.ManyToManyField(Tag)
    # 定休日（中間フィールド）
    regular_holidays = models.ManyToManyField(Weekday, through=Regular_holidays, related_name='shops_set_holidays')

    # 公開
    is_published = models.BooleanField(default=False, verbose_name='公開')
    # 作成・更新日時
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # インスタンスの生成（returnでnameを返すことで、一覧画面で名前が表示される）
    def __str__(self):
        return self.name
