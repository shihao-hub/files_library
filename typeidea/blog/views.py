from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView, ListView

from blog.models import Post, Tag, Category
from config.models import SideBar


# Create your views here.

class CommonViewMixin:
    def get_context_data(self, **kwargs):
        """
        这边存储通用数据，子类继承重新即可（重写的时候调用一下基类的函数）
        """
        context = super().get_context_data(**kwargs)
        context.update({
            "sidebars": SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = "post_list"
    template_name = "blog/list.html"


class CategoryView(IndexView):
    """
    Category 导航栏，和 IndexView 一个样
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")  # 这个 self.kwargs 是请求时传入 view 函数的参数
        category = get_object_or_404(Category, pk=category_id)  # TODO: 为什么是 pk
        context.update({
            "category": category
        })
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        return qs.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id")  # 这个 self.kwargs 是请求时传入 view 函数的参数
        tag = get_object_or_404(Category, pk=tag_id)  # TODO: 为什么是 pk
        context.update({
            "tag": tag
        })
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return qs.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = "blog/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"
