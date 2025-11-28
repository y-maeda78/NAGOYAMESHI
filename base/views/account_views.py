from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from base.models import Profile
# from base.forms import UserCreationForm
from base.forms import CustomUserCreationForm, ProfileForm # 修正：フォーム名変更のため
from django.db import transaction # 追加
from django.contrib import messages
from django.shortcuts import render, redirect # 追加
 
# 新規登録のビュー
class SignUpView(CreateView):
    # form_class = UserCreationForm
    form_class = CustomUserCreationForm # 修正：フォーム名変更のため
    success_url = '/login/'
    template_name = 'pages/signup.html'

    # 追加：contextにProfileFormを追加
    def get_context_data(self, **kwargs):

        if not hasattr(self, 'object'):
            self.object = None

        context = super().get_context_data(**kwargs)

        if 'form' not in kwargs:
            context['form'] = self.get_form() # CustomUserCreationForm

        if 'profile_form' not in context:
            context['profile_form'] = ProfileForm()

        context.update(kwargs)
        
        return context
    
    # 追加：フォームの処理
    def post(self, request, *args, **kwargs):
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            return self.forms_valid(user_form, profile_form)
        else:
            return self.forms_invalid(user_form, profile_form)
    
    # 追加
    @transaction.atomic
    def forms_valid(self, user_form, profile_form):
        # Userモデルを保存
        self.object = user_form.save()
        
        # Profileモデルを保存
        profile = profile_form.save(commit=False)
        profile.user = self.object # ユーザーとProfileを紐づけ
        profile.save()        

    # 新規登録が有効だった場合
    def form_valid(self, form):
        messages.success(self.request, '新規登録が完了しました。続けてログインしてください。')
        return super().form_valid(form)
    
    # 追加：エラーの場合（両方のフォームをコンテキストに戻す）
    def forms_invalid(self, user_form, profile_form):
        return self.render_to_response(self.get_context_data(form=user_form, profile_form=profile_form))
    def form_valid(self, form):
        messages.success(self.request, '入力内容に誤りがあります。再度確認してください。')
        return super().form_valid(form)
 
 
class Login(LoginView):
    template_name = 'pages/login.html'
 
    def form_valid(self, form):
        messages.success(self.request, 'ログインしました。')
        return super().form_valid(form)
 
    def form_invalid(self, form):
        messages.error(self.request, 'エラー：ログインできません。')
        return super().form_invalid(form)
 
# アカウントの編集
# LoginRequiredMixin:ログインしていなければ見えない 
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ('username', 'email',)
    success_url = '/account/'  # 更新した際にどこのページに飛ばすか（この場合は今のページにとどまる）
 
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()
 
# LoginRequiredMixin:ログインしていなければ見えない
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    fields = ('name', 'zipcode', 'prefecture',
              'city', 'address1', 'address2', 'tel')
    success_url = '/profile/'  # 更新した際にどこのページに飛ばすか（この場合は今のページにとどまる）
 
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()