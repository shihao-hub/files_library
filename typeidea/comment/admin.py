from django.contrib import admin


from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from .adminforms import CommentAdminForm
from .models import Comment


# Register your models here.

@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ("target", "content", "website", "nickname", "email", "created_time", "owner")

    form =CommentAdminForm
    # fields 为空的时候似乎会自动填充成全部字段
