import os.path
import mimetypes
from datetime import date

from django.conf import settings
from django.core.cache import cache  # FIXME: 请配置一下，如果不配置，使用的是内存！
from django.db.models import F, Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView, ListView

from blog.models import Post, Tag, Category, Download
from config.models import SideBar


# Create your views here.

class CommonViewMixin:
    """通用集
    这里很重要，非常重要。难受的点是，super().get_context_data 调用的问题。
    只有继承该类的子类还有其他基类，那个基类有这个函数才行。所以这里 pycharm 会警告没有这个函数。
    """

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
    queryset = Post.get_posts()
    paginate_by = 5  # 分页功能，至于分谁的页，应该是 queryset 这个数据的页
    context_object_name = "post_list"
    template_name = "blog/list.html"


# ----------------------------------------------------------------------- nav
class CategoryView(IndexView):
    """
    Category 导航栏，和 IndexView 一个样
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")  # 这个 self.kwargs 是请求时传入 view 函数的参数
        category = get_object_or_404(Category, pk=category_id)
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
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            "tag": tag
        })
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return qs.filter(tag__id=tag_id)


# ----------------------------------------------------------------------- others
class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "keyword": self.request.GET.get("keyword", "")
        })
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        kw = self.request.GET.get("keyword")
        if not kw:
            return qs
        return qs.filter(
            Q(title__icontains=kw)
            | Q(desc__icontains=kw)
            | Q(content__icontains=kw)
        )


class AuthorView(IndexView):
    def get_queryset(self):
        qs = super().get_queryset()
        author_id = self.kwargs.get("author_id")
        print(author_id)
        return qs.filter(owner_id=author_id)


# ----------------------------------------------------------------------- post-detail
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = "blog/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handler_visited()
        return response

    def handler_visited(self):
        """此处实现了之后，不方便测试了！因为每次浏览一分钟才能计数
        """
        increase_pv, increase_uv = False, False
        uid = self.request.uid
        pv_key = "pv:{}:{}".format(uid, self.request.path)
        uv_key = "pv:{}:{}:{}".format(uid, str(date.today()), self.request.path)

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F("pv") + 1, uv=F("uv") + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F("pv") + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F("uv") + 1)


# ----------------------------------------------------------------------- views
class DownloadView(ListView):
    """
    FIXME: 该类由本人自己实现，因此抽象的并不好，记得优化
    """
    queryset = Download.objects.all()
    template_name = "common/download.html"
    context_object_name = "download_list"

    # 不需要这个函数
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     # print(args, kwargs) # url 为 /download/ 时，打印 -> (),{}
    #     if kwargs == {}:
    #         return context
    #
    #     file_id = self.kwargs.get("file_id")
    #     file_path = get_object_or_404(Download, pk=file_id)
    #     context.update({
    #         "file_path": file_path
    #     })
    #     return context

    def get(self, request, *args, **kwargs):
        # print(request, args, kwargs)  # url 为 /download/ 时，打印 -> <WSGIRequest: GET '/download/'>,(),{}
        # 查询字段在 request.GET 里！
        # try:
        #     print(request.GET)
        # except Exception as e:
        #     print(e)
        if kwargs == {}:
            return super().get(request, *args, **kwargs)

        # 这样修改 get，通过 kwargs 判断合理吗？ Ans: 就目前来说，我觉得还行。需求我已经是实现了。
        file_id = self.kwargs.get("file_id")
        download = get_object_or_404(Download, pk=file_id)

        file_path = os.path.join(settings.MEDIA_ROOT, download.path)
        filename = os.path.basename(file_path)
        # file_extension = os.path.splitext(file_path)[1] or ""

        content_type, _ = mimetypes.guess_type(filename)

        if not content_type:
            content_type = "application/octet-stream"

        # print(content_type)

        # 这么麻烦？所以 python 应该有库帮我实现好了吧？ -> YES，随便查一下有个 mimetypes 内置库，其他的暂且未知
        # if file_extension == ".docx":
        #     file_extension = "vnd.openxmlformats-officedocument.wordprocessingml.document"
        # elif file_extension:
        #     file_extension = file_extension[1:]

        # print(file_path, filename, file_extension)

        with open(file_path, "rb") as file:
            response = HttpResponse(file.read(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            return response
