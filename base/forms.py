from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm # 追加：複数モデルを使用するために追加
from base.models import Profile # 追加：profileモデルをインポート
 
# class UserCreationForm(forms.ModelForm):
class CustomUserCreationForm(DjangoUserCreationForm): # 修正：複数モデルを使用するため
    password = forms.CharField()
 
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
        )
 
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# 同時にprofileのフォームを処理する
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
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


