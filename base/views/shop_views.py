from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Shop, Category, Tag, Favorite
from django.db.models import Avg, Q, Count
from django.shortcuts import get_object_or_404, redirect

class IndexListView(ListView):
    model = Shop
    template_name = 'pages/index.html'

# 詳細ページ
class ShopDetailView(DetailView):
    model = Shop
    template_name = 'pages/restaurants_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user
        shop = get_object_or_404(Shop, pk=self.kwargs['pk'])
        if user_obj.is_authenticated:
            context['favorites'] = Favorite.objects.filter(user=self.request.user, shop=shop).count()
        else:
            context['favorites'] = 0

        return context



# 検索した際に表示する店舗一覧ページ
class ShopListView(ListView):
    model = Shop
    template_name = 'pages/restaurants_list.html'
    # ordering = 'created_at' #新規掲載順
    paginate_by = 10   # 1ページにいくつ表示するか

    """
    # vegeket参考
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(
        is_published=True, category=self.category)    # is_published=True：公開されているものだけを表示

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"カテゴリー： #{self.category.name}"
        return context
    """


    # キーワード検索
    def get_context_data_keyword_search(self, context):  
        keyword = self.request.GET.get('keyword')
        if keyword is not None and not '':
            query = Q()
            words = keyword.replace('　', ' ').split(' ')
            for word in words:
                if word == " ":
                    continue
            
                query &= Q(category__name__contains=word) | Q(detail__contains=word) | Q(name__contains=word) | Q(address__contains=word)
            
            context['shops'] = Shop.objects.filter(query)

    # カテゴリ検索
    def get_context_data_category_search(self, context):        
        context['categories'] = Category.objects.all()
        category_id = self.request.GET.get('category_id')
        if category_id is not None and not '':
            context['category_id'] = int(category_id)
            context['shops'] = Shop.objects.filter(Q(category__id=category_id) | Q(category2__id=category_id) | Q(category3__id=category_id))

    # タグ検索
    def get_context_data_tag_search(self, context):
        context['tags'] = tag.objects.all()
        tag_id = self.request.GET.get('tag_id')
        if tag_id is not None and not '':
            context['tag_id'] = int(tag_id)
            context['shops'] = Shop.objects.filter(Q(tag__id=category_id) | Q(tag2__id=category_id) | Q(tag3__id=category_id))

    # 料金検索
    def get_context_data_price_search(self, context):        
        context['prices'] = range(500, 10001, 500)
        price = self.request.GET.get('price')
        if price is not None and not '':
            context['sprice'] = price
            context['shops'] = Shop.objects.filter(budget_min__lte=context['sprice'] , budget_max__gte=context['sprice'])

    # 表示順
    def get_context_data_sort_order(self, context):
        context['sort_order'] = { 'created_at desc':'掲載日が新しい順', 'price asc':'価格が安い順', 'rating desc':'評価が高い順', 'popular desc':'予約数が多い順', }
        select_sort = self.request.GET.get('select_sort')
        if select_sort is not None and not '':
            context['selected_sort'] = select_sort

            if select_sort == 'created_at desc':
                context['shops'] = context['shops'].order_by('-created_at')
            elif select_sort == 'price asc':
                context['shops'] = context['shops'].order_by('budget_min')
            elif select_sort == 'rating desc':
                context['shops'] = context['shops'].annotate(average_stars = Avg('reviews__stars')).order_by('-average_stars')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 店舗
        context['shops'] = Shop.objects.all()

        # キーワード検索
        self.get_context_data_keyword_search(context)

        # カテゴリ検索
        self.get_context_data_category_search(context)

        # 料金検索
        self.get_context_data_price_search(context)

        # 表示順
        self.get_context_data_sort_order(context)
        
        return context

