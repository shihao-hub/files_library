from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    继承该类的话：
        1. 保存的时候自动存储 owner
        2. 获取列表的时候只获取当前用户创建的数据
    """
    exclude = ("owner",)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     qs = super(BaseOwnerAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)
