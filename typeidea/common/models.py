from django.db import models


# Create your models here.


class UploadPost(models.Model):
    file_path = models.CharField(max_length=266, verbose_name="文件路径")

    class Meta:
        verbose_name = verbose_name_plural = "文件路径"


class ServiceRunTime(models.Model):
    total = models.DateTimeField()