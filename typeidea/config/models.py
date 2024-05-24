from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string


# Create your models here.

class Link(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "友链"

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")  # 默认长度为 200
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    weight = models.PositiveIntegerField(default=1,
                                         choices=zip(range(1, 6), range(1, 6)),
                                         verbose_name="权重",
                                         help_text="权重高展示顺序靠前")

    owner = models.ForeignKey(User, models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


class SideBar(models.Model):
    """侧边栏
    """
    objects = models.Manager()

    class Meta:
        """
        这个类的作用是：配置 Model 的属性
        """
        verbose_name = verbose_name_plural = "侧边栏"

    DISPLAY_HTML, DISPLAY_LATEST, DISPLAY_MOST_HOT, DISPLAY_COMMENT = (1, 2, 3, 4)
    STATUS_SHOW, STATUS_HIDE = (1, 0)
    STATUS_ITEMS = ((STATUS_SHOW, "展示"), (STATUS_HIDE, "隐藏"))
    SIDE_TYPE = zip(range(1, 5), ["HTML", "最新文章", "最热文章", "最近评论"])

    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(default=1,
                                               choices=SIDE_TYPE,
                                               verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, verbose_name="内容",
                               help_text="如果设置的不是 HTML 类型，可为空")
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        # 避免循环依赖，用到的时候再导入
        from blog.models import Post
        from comment.models import Comment

        result = ""

        # 四种情况全部返回 html
        dt = self.display_type
        if dt == self.DISPLAY_HTML:
            result = self.content
        elif dt == self.DISPLAY_LATEST:
            result = render_to_string(
                "config/blocks/sidebar_posts.html",
                {"posts": Post.latest_posts()}
            )
        elif dt == self.DISPLAY_MOST_HOT:
            result = render_to_string(
                "config/blocks/sidebar_posts.html",
                {"posts": Post.most_hot_posts()}
            )
        elif dt == self.DISPLAY_COMMENT:
            result = render_to_string(
                "config/blocks/sidebar_comments.html",
                {"comments": Comment.objects.filter(status=Comment.STATUS_NORMAL)}
            )

        return result
