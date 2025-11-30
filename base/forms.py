from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm 
from django.contrib.auth.forms import AuthenticationForm # 追加：認証するため
# from django.contrib.auth.forms import PasswordChangeForm # パスワード変更専用
 
User = get_user_model()

# class UserCreationForm(forms.ModelForm):
class CustomUserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
 
# ユーザー情報更新用フォーム
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "tel",
            "zipcode",
            "prefecture",
            "city",
            "address1",
            "address2",
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrapのスタイルを適用
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
"""
# パスワード変更専用フォーム
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
"""


# 追加 メールアドレス認証用フォーム
class EmailAuthenticationForm(AuthenticationForm):

    username = forms.CharField(widget=forms.HiddenInput(), required=False) # 必須ではない隠しフィールドとして再定義
    email = forms.EmailField(label='メールアドレス', max_length=254,
                                widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレス'}))

    def clean(self):
        # この clean メソッド内で、メールアドレスをユーザー名として扱い、
        # 親クラスの AuthenticationForm が DB を検索・認証します
        email = self.cleaned_data.get('email')
        if email:
            self.cleaned_data['username'] = email
        return super().clean()