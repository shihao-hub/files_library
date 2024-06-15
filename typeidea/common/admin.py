from django.contrib import admin

from common.models import UploadPost
from typeidea.custom_site import custom_site


@admin.register(UploadPost, site=custom_site)
class UploadPostAdmin(admin.ModelAdmin):
    list_display = ("file_path",)