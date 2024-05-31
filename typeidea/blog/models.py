import mistune as mistune
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


# Create your models here.


class Category(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        qs = cls.objects.filter(status=cls.STATUS_NORMAL)
        is_nav, normal = [], []  # 放入内存，避免多次访问数据库
        for e in qs:
            if e.is_nav:
                is_nav.append(e)
            else:
                normal.append(e)
        return {
            "navs": is_nav,
            "categories": normal
        }


class Tag(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name


class Download(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "下载文件"

    name = models.CharField(max_length=260, verbose_name="名称")
    # path = models.FilePathField(verbose_name="文件路径")
    path = models.CharField(max_length=260, verbose_name="文件路径")

    def __str__(self):
        return self.name


class Post(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"), (STATUS_DRAFT, "草稿"))

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")  # blank 是业务端可为空，null 是数据库端可为空
    content = models.TextField(verbose_name="正文", help_text="正文必须为 MarkDown 格式")
    content_html = models.TextField(verbose_name="正文 html 代码", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, models.CASCADE, verbose_name="分类")  # 外键自动添加个 category_id ？
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    pv = models.PositiveIntegerField(default=1)  # 点击量
    uv = models.PositiveIntegerField(default=1)  # 这是？

    def __str__(self):
        return "{}-{}-{}".format(self.title, self.category, self.created_time)

    def save(self, *args, **kwargs):
        # FIXME：添加了 ckeditor 插件之后，不可以再调用 markdown 了，他那边会自动转为 markdown？
        #   呃，你用 **abc** 这种代码也不行了！可恶啊！果然 Typora 的含金量还是在的！
        self.content_html = mark_safe(mistune.markdown(self.content))
        # print(self.content)
        # print(self.content_html) # debug 模式打印还差不多
        super().save(*args, **kwargs)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @staticmethod
    def get_by_tag(tag_id):
        post_list = []
        tag = None
        if tag_id:
            try:
                tag = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                pass
            else:
                post_list = tag.post_set \
                    .filter(status=Post.STATUS_NORMAL) \
                    .select_related("owner", "category")
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        post_list = []
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
            else:
                post_list = category.post_set \
                    .filter(status=Post.STATUS_NORMAL) \
                    .select_related("owner", "category")
        return post_list, category

    @staticmethod
    def get_posts_order_by(order_by, filter_status=None, select_related_list=("owner", "category")):
        if not filter_status:
            filter_status = Post.STATUS_NORMAL
        queryset = Post.objects \
            .filter(status=filter_status) \
            .order_by(order_by) \
            .select_related(*select_related_list)
        return queryset

    @classmethod
    def get_posts(cls):
        return cls.objects \
            .filter(status=cls.STATUS_NORMAL) \
            .order_by("-created_time") \
            .select_related("owner", "category")

    @classmethod
    def latest_posts(cls):
        # FIXME: 在这里切片的话会报错 [:5]？
        return cls.get_posts_order_by("-created_time")

    @classmethod
    def most_hot_posts(cls):
        return cls.get_posts_order_by("-pv")
