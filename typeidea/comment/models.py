import mistune
from django.db import models
from django.contrib.auth.models import User

from blog.models import Post


# Create your models here.

class Comment(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "评论"

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    # target = models.ForeignKey(Post, models.CASCADE, verbose_name="评论目标")
    target = models.CharField(max_length=100, verbose_name="评论目标")
    content = models.CharField(max_length=2000, verbose_name="内容", help_text="内容支持 MarkDown 格式")
    content_html = models.CharField(max_length=2000, verbose_name="内容", blank=True, editable=False)
    nickname = models.CharField(max_length=200, verbose_name="昵称", default="佚名")
    website = models.URLField(verbose_name="网站")
    email = models.EmailField(verbose_name="邮箱")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    owner = models.ForeignKey(User, models.CASCADE, verbose_name="作者", null=True)

    @classmethod
    def get_by_target(cls, target, order_by_str=None):
        res = cls.objects.filter(target=target, status=Comment.STATUS_NORMAL)
        if not order_by_str:
            return res
        return res.order_by(order_by_str)

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)
