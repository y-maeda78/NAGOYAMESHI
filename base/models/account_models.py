"""
カスタマイズユーザーモデルを定義
"""

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .shop_models import create_id

# ユーザーモデル
class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username,            
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.CharField(default=create_id, primary_key=True, max_length=22)
    username = models.CharField(
        max_length=50, unique=True, verbose_name='ユーザー名')
    email = models.EmailField(max_length=255, unique=True, verbose_name='メールアドレス')
    is_paymentstatus = models.BooleanField(default=False, verbose_name='有料会員')
    is_deleted = models.BooleanField(default=False, verbose_name='削除状態')
    is_admin = models.BooleanField(default=False, verbose_name='管理者権限')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# ユーザーのプロフィール情報
class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    # OneToOneField：1対1の関係性、ユーザーAに対してプロフィールA

    # 名前(ユーザーネームを使う仕様にしてもOK)
    name = models.CharField(default='', blank=True, max_length=50, verbose_name='名前')
    zipcode = models.CharField(default='', blank=True, max_length=8, verbose_name='郵便番号')
    prefecture = models.CharField(default='', blank=True, max_length=50, verbose_name='都道府県')
    city = models.CharField(default='', blank=True, max_length=50, verbose_name='市町村')
    address1 = models.CharField(default='', blank=True, max_length=50, verbose_name='住所1 丁目・番地・号')
    address2 = models.CharField(default='', blank=True, max_length=50, verbose_name='住所2 マンション・アパート名')
    # birthday = models.DateField(null=True, blank=True, verbose_name='誕生日')
    tel = models.CharField(default='', blank=True, max_length=15, verbose_name='電話番号')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# OneToOneField を同時に作成　ユーザーモデルが作成されたらプロフィールが作成される仕様
# @：デコレーター　関数が実行される前に ＠～ の処理を実行する
@receiver(post_save, sender=User)         # ユーザーモデルが作成されたタイミングで
def create_onetoone(sender, instance, created, **kwargs):    # プロフィールを作成する
    if created: 
            Profile.objects.create(
                user=instance, 
                name=instance.username 
            )