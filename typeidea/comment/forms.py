from ckeditor.widgets import CKEditorWidget
from django import forms

from comment.models import Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ("nickname", "email", "website", "content",)
        # fields = ("nickname", "content",)
        fields = ("content",)

    # nickname = forms.CharField(
    #     label="昵称",
    #     max_length=50,
    #     widget=forms.widgets.Input(
    #         attrs={
    #             "class": "form-control",
    #             "styles": "width: 60%;"
    #         }
    #     )
    # )
    # email = forms.EmailField(
    #     label="你的个人邮箱",
    #     max_length=50,
    #     widget=forms.widgets.EmailInput(
    #         attrs={
    #             "class": "form-control",
    #             "styles": "width: 60%;"
    #         }
    #     )
    # )
    # website = forms.URLField(
    #     label="网站",
    #     max_length=100,
    #
    #     widget=forms.widgets.URLInput(
    #         attrs={
    #             "class": "form-control",
    #             "styles": "width: 60%;"
    #         }
    #     )
    # )
    content = forms.CharField(
        label="",
        max_length=500, # 虽然数据库可以存 2000，但是表单验证，可以更少。（那么意义是什么呢？）
        # widget=forms.widgets.Textarea(
        #     attrs={
        #         "rows": 6,
        #         "cols": 60,
        #         "class": "form-control"
        #     }
        # ),
        # 不行，这只是 widget，似乎还缺少插件？
        widget=CKEditorWidget(),
        required=True,
    )

    def clean_content(self):
        content = self.cleaned_data.get("content")

        # 长度
        if len(content) <= 10:
            raise forms.ValidationError("内容怎么能这么短呢！")

        # 敏感词
        # 学习使用（Java）：https://blog.csdn.net/weixin_39666736/article/details/104903518
        # 学习使用：https://blog.csdn.net/u013421629/article/details/83178970

        return content
