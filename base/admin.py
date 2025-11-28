from django.contrib import admin
from base.models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
# from base.forms import UserCreationForm
from base.forms import CustomUserCreationForm # 修正：フォーム名変更のため
from django import forms  # 追記
import json  # 追記
 
 
class TagInline(admin.TabularInline):
    model = Shop.tags.through
 
 
class ShopAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags']

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    # 管理画面のUser詳細画面で表示される項目
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (None, {'fields': ('is_paymentstatus', 'is_active', 'is_admin',)})
    )

    # 管理画面のUser一覧で表示される項目
    list_display = ('username', 'id', 'is_admin', 'is_active', 'updated_at',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()

    # --- adminでuser作成用に追加 ---
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
    )
    # --- adminでuser作成用に追加 ---

    # add_form = UserCreationForm
    add_form = CustomUserCreationForm # 修正：フォーム名変更のため

    # profileの内容をインラインとしてUser画面に表示する
    inlines = (ProfileInline,)
 
admin.site.register(Shop, ShopAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)