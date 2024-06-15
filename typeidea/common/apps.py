from datetime import datetime

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'

    # NOTE: 此处有奇怪的地方，
    #   runserver -> ready 函数会被执行两次，一次应该是数据库的时候
    #   migrate -> ready 执行一次，on_startup 执行好多次... 我目前测试的时候运行了 6、7 次...
    # def ready(self):
    #     # 注册应用启动信号的处理函数
    #     @receiver(post_migrate)
    #     def on_startup(sender, **kwargs):
    #         # 在这里执行您希望在启动时执行的代码
    #         print("应用启动了，现在执行初始化代码")
    #
    #     if not getattr(self, 'initialized', False):
    #         from common.models import ServiceRunTime
    #         print("应用启动了，现在执行初始化代码2")
    #         ServiceRunTime.objects.create(total=datetime.now())
    #         print(ServiceRunTime.objects.all())
    #         self.initialized = True
