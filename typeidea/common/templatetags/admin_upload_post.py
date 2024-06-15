from django import template

from common.forms import UploadPostForm

register = template.Library()


@register.inclusion_tag("common/admin_upload_post.html")
def admin_upload_post():
    return {
        "form": UploadPostForm()
    }
