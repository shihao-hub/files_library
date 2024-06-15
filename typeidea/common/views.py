import pprint

from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view

from blog.models import Post
from common.forms import UploadPostForm


# Create your views here.

# rest_framework 的使用方法要注意
# @api_view(["POST"])
def upload_post_view(request):
    template_name = "common/admin_upload_post.html"

    if request.method == "GET":

        try:
            post_id = request.GET["post_id"]
            form = UploadPostForm(initial={"post_id": post_id})
        except KeyError:
            form = UploadPostForm()
            return HttpResponseBadRequest("Error: there is no `post_id` field in the query parameter")
        context = {
            "succeed": "GET_true",
            "form": form
        }
        return render(request, template_name, context)
    elif request.method == "POST":
        form = UploadPostForm(request.POST)

        # NOTE: request.POST 是 dict 的子类，form 打印出来的是 html 文本
        pprint.pprint(request.POST)
        # print(form)

        succeed = "POST_true"
        msg = ""

        post_id = request.POST["post_id"]
        file_path = request.POST["file_path"]

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                obj = Post.objects.get(id=post_id)
                if obj:
                    obj.content = file.read()
                    obj.save()
        except FileNotFoundError as e:
            succeed = "POST_false"
            msg = str(e)

        context = {
            "succeed": succeed,
            "form": form,
            "msg": msg
        }
        return render(request, template_name, context)
