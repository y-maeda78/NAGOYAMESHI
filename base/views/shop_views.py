from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Shop, Category, Tag

class IndexListView(ListView):
    model = Shop
    template_name = 'pages/index.html'