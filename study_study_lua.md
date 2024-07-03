**2024-07-03**

总结一下今日的学习内容：



- Lua for Windows 很久没更新了，它的各种库的介绍页也打不开了，所以应该试着找其他工具库使用。
- luarocks 类似 Python 的 pip，需要学习一下如何使用。
- awesome-lua 稍微看了看找到了两个库，lua-stdlib 和 30log，这两个库应该是需要从 luarocks 上下载下来使用的。回头记得实战一下。
- 不得不说，Lua 还是很不错的，Python 和 Lua 我都要完完全全地掌握！
-  IDEA 的 EmmyLua 插件可以从手机下载发到电脑上。我发现，默认的 EmmyLua 的代码风格很适合 Lua 呀，家里的 EmmyLua 改了好多，得改回来！



**1.** Lua for Windows 很久没更新了，它的各种库的介绍页也打不开了，所以应该试着找其他工具库使用。

**2.** luarocks 类似 Python 的 pip，需要学习一下如何使用。

**3.** awesome-lua 稍微看了看找到了两个库，lua-stdlib 和 30log，这两个库应该是需要从 luarocks 上下载下来使用的。回头记得实战一下。

**4.** 不得不说，Lua 还是很不错的，Python 和 Lua 我都要完完全全地掌握！

**5.** IDEA 的 EmmyLua 插件可以从手机下载发到电脑上。我发现，默认的 EmmyLua 的代码风格很适合 Lua 呀，家里的 EmmyLua 改了好多，得改回来！



太棒了，python lua 交互（太简单了，Python 你是我的神）

```python
import lupa

from lupa.lua51 import LuaRuntime

lua = LuaRuntime()

lua.execute("""
package.path = ";D:\\\\shzhang\\\\IdeaProjects\\\\Lua\\\\src\\\\?.lua" .. package.path
require("main")
""")

```

只需要上面这段代码，python lua 就联系起来了！

想一想，饥荒的 C++ 和 Lua 脚本，C++ 作为引擎，启动 Lua 的 main.lua 文件。

太妙了，太爱了。
