from django import forms

from blog.models import Post

from ckeditor.widgets import CKEditorWidget


# 不是在这里，而是在 PostAdminForm 里。但是话说这个作用在哪里啊？
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ("title", "desc", "content", "category", "status", "tag")
#
#     content = forms.CharField(widget=CKEditorWidget(), label="正文", required=True)
