import os

import lupa
from lupa.lua51 import LuaRuntime


lua = LuaRuntime()
lua_g = lua.globals()

lua_g["list"] = list
lua_g["os_walk"] = os.walk
lua.execute("""\
package.path = ";E:\\\\ProgrammingProjects\\\\IDEAProjects\\\\Lua\\\\lua_start_project\\\\src\\\\?.lua" .. package.path
require("lupa_test")
""")
