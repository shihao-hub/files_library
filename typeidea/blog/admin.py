from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # 注意看一下 django.contrib.admin.options/ModelAdmin/log_addition 函数
    list_display = (
        "user_id",
        "content_type_id",
        "object_id",
        "object_repr",
        "action_flag",
        "change_message",
    )


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "is_nav", "created_time", "post_count", "owner")  # 展示的内容
    fields = ("name", "status", "is_nav")  # 需要填写的内容

    def post_count(self, obj):
        # 由于 Post Model 中的字段与 Category 有关联，
        # 所以 Category 中可以通过 post_set 这种方式获取到相关内容（猜测的，因为 Tag 也可以这样获取）
        return obj.post_set.count()

    post_count.short_description = "相关文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "created_time", "post_count", "owner")
    fields = ("name", "status")

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "相关文章数量"


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "分类"
    parameter_name = "owner_category_id"

    def lookups(self, request, model_admin):
        # filter 保证查询到的都是发送请求的用户，不可以显示其他用户的信息
        res = Category.objects.filter(owner=request.user).values_list("id", "name")
        # print("lookups->", res)
        return res

    def queryset(self, request, queryset):
        # 刷新页面或者点击过滤按钮时会执行此处，
        # self.value() 应该就是 url 中的 ?xxx=y 中的 y，如果不存在则返回 None
        category_id = self.value()
        # print("queryset->", category_id)
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    # class Media:
    #     css = {
    #         "all": (
    #             "https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
    #         )
    #     }
    #     js = (
    #         "https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",
    #     )
    form = PostAdminForm

    list_display = ["title", "category", "status", "operator", "pv", "uv", "created_time", "owner"]
    list_display_links = []

    list_filter = [CategoryOwnerFilter, "status"]
    search_fields = ["title", "category__name"]

    actions_on_top = True
    # actions_on_bottom = True

    # save_on_top = True # 控制 保存|保存并增加另一个|保存并继续编辑 是否放在上方

    # fields 是表单要填写的内容，以下面这个结构来说，第一行有两项，下面每行各一项。
    # fields = (
    #     ("category", "title"),
    #     "desc",
    #     "status",
    #     "content",
    #     "tag",
    # )

    # exclude = ("owner",) #?

    # 和 fields 不可同时存在：Both 'fieldsets' and 'fields' are specified.
    fieldsets = (
        ("基础配置", {
            "description": "基础配置描述",
            "fields": (
                ("category", "title",),
                "status",
            )
        }),
        ("内容", {
            "fields": (
                "desc",
                "content",
            )
        }),
        ("额外信息", {
            "classes": ("collapse",),
            "fields": ("tag",)
        })
    )

    # filter_vertical = ("category", "title",) The value of 'filter_vertical[0]' must be a many-to-many field.

    def operator(self, obj):
        """自定义操作，返回值即为显示的值，因此生成 html 的话，可以提供点击功能！"""
        return format_html('<a href = "{}">编辑</a>', reverse("cus_admin:blog_post_change", args=(obj.id,)))

    # ? Python 也能和 Java 一样吗？这里是不是类似 Java 的 static {}
    operator.short_description = "操作"

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
