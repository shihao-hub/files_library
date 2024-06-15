#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from datetime import datetime


def main():
    """Run administrative tasks."""
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'typeidea.settings')
    profile = os.environ.get("TYPEIDEA_PROFILE", "develop")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "typeidea.settings.%s" % profile)

    from django.core.management.commands.runserver import Command as Runserver
    Runserver.default_port = "1060"  # 修改默认端口

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # NOTE: 此处应该在 While True，故 main() 下面的内容只有在中断的时候才会之前，而且会执行两遍？
    #   罢了，不捣鼓了，浪费时间。有这功夫看看书都比这好，毕竟半吊子的捣鼓就是浪费时间！
    main()
