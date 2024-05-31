from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from comment.forms import CommentForm


# Create your views here.


class CommentView(TemplateView):
    http_method_names = ("post",)
    template_name = "comment/result.html"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        # 表单的 name 属性就是 sumit 的时候 url 的查询条件的键值
        target = request.POST.get("target")
        succeed = False

        if comment_form.is_valid():
            inst = comment_form.save(commit=False)
            inst.target = target  # 存一下评论目标
            inst.save()
            succeed = True
            # return redirect(target) # 没必要重定向吧？

        return self.render_to_response({
            "succeed": succeed,
            "form": comment_form,
            "target": target
        })
