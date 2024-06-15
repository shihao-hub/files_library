"""
URL configuration for typeidea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.contrib import admin
from django.urls import path, re_path, include

from blog.views import IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthorView, DownloadView
from comment.views import CommentView
from config.views import LinkListView

from .custom_site import custom_site

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name="home-page"),

    re_path(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name="category-list"),

    re_path(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name="tag-list"),
    re_path(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name="post-detail"),

    re_path(r'^search/$', SearchView.as_view(), name="search"),

    # TODO: 这个没什么用啊
    re_path(r'^author/(?P<author_id>\d+).html$', AuthorView.as_view(), name="author"),

    # NOTE: form 的 action -> 规定当提交表单时，向何处发送表单数据。
    re_path(r'^comment/$', CommentView.as_view(), name="comment"),

    re_path(r'^download/$', DownloadView.as_view(), name="download"),

    # 强调一点，此处调用 view 函数的时候，模式匹配的 file_id 会以查询字段 file_id=x 的方式传入 view 函数
    re_path(r'^download/(?P<file_id>\d+)$', DownloadView.as_view(), name="download"),
    # FIXME：必须 download，否则匹配不上。
    #  html 中 reverse 的时候匹配有问题，
    #  {% url 'download' param %} 中的 'download' 好像就是这个 pattern，param 就是传进去的参数...
    #  怎么出错的：r'^download/$' 却传入的参数 ...

    re_path(r'^links/$', LinkListView.as_view(), name="links"),

    # NOTE: 这个 name 有什么用呢？
    path("common/", include("common.urls"), name="common"),

    path('super_admin/', admin.site.urls, name="super-admin"),
    path('admin/', custom_site.urls, name="admin"),
]
