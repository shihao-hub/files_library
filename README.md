Restful -> 将一切视为资源

GET posts -> 所有文章

GET posts/1 -> 某篇文章

POST posts -> 创建文章

PUT posts/1 -> 更新文章

DELETE posts/1 -> 删除文章

POST posts/actions/beautify -> 非增删改查的特殊动作



1. django 的源代码目录为当前目录下的 typeidea，因此请用 PyCharm 的右键功能将其标记为源代码目录
    ```txt
   -- typeidea -> 项目
   ---- CHANGELOG.md
   ---- README.md
   ---- requirements.txt
   ---- typeidea -> 项目源代码目录，因此使用 PyCharm 打开时，需要将其设置为源代码目录
   ------ typeidea -> app
   ------ blog -> app
   ------ comment -> app
   ------ config -> app
    ```

2. 奠定项目的基石：Model
    ```txt
   1. 配置 setting，将 setting.py -> setting 模块，所以还需要 wsgi.py manager.py 中的环境变量的值
   2. 创建 Model 层，在 app 的 models.py 文件中创建数据类
   3. 配置 settings 中的 INSTALLED_APPS，将自己的 app 放在列表前面
   4. 创建数据库表
        执行以下操作：
            py manage.py makemigrations ->创建迁移文件
            py manage.py migrate -> 执行迁移操作
        此后，目录下将会出现个 db.sqlite3（这个名字可以自己定义）二进制文件，这应该就是数据库文件。
   5. 执行 py manage.py runserver 即可运行起来，但是由于未配置 urls，
   所以 http://127.0.0.1:8000/ 没有任何内容，但是 http://127.0.0.1:8000/admin/ 管理页面是存在的。
   PS: py manage.py createsuperuser 可以用来创建管理员账户
   
    ```

3. 开发管理后台
    ```txt
   
    ```