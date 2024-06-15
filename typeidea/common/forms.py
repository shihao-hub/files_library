from django import forms

from blog.models import Post
from common.models import UploadPost


class UploadPostForm(forms.Form):
    post_id = forms.IntegerField(
        label="文章编号",
        widget=forms.widgets.Input(
            attrs={
                "class": "form-control",
                "styles": "width: 60%;"
            }
        )
    )

    file_path = forms.CharField(
        label="文件路径",
        max_length=266,
        widget=forms.widgets.Input(
            attrs={
                "class": "form-control",
                "styles": "width: 60%;"
            }
        )
    )
