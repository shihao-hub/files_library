from django.urls import path, re_path, include

import common.views as views

urlpatterns = [
    path("admin_blog_post/upload_post.html", views.upload_post_view, name="common-upload_post")
]
