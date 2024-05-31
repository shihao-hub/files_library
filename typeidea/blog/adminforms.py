from django import forms

from ckeditor.widgets import CKEditorWidget

# django 并不知道这个文件中的这个类，之所以知道是因为给 PostAdmin 的 form 属性赋值了！
class PostAdminForm(forms.ModelForm):
    # 这个不好看
    # desc = forms.CharField(widget=forms.Textarea, label="摘要", required=False)
    content = forms.CharField(widget=CKEditorWidget(), label="正文", required=True)

