from django import forms

from ckeditor.widgets import CKEditorWidget


class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="正文", required=True)
