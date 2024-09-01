import enum
import re
from types import SimpleNamespace


class SetPrivatePropertyMixin:
    private_set = set()

    def add_private(self, name):
        self.private_set.add(name)

    def remove_private(self, name):
        self.private_set.remove(name)

    def __getattribute__(self, item):
        if item in self.private_set and item != "private_set":
            raise AttributeError(f"'{self.__class__.name}' object has no attribute '{item}'")
        if isinstance(item, str) and item.startswith(":"):
            item = item[1:]

        return super().__getattribute__(item)


class Dog(SetPrivatePropertyMixin):

    def __init__(self):
        self.add_private("say")

    def say(self):
        pass


class Status(enum.Enum):
    # 创建态、就绪态、阻塞态、运行态、终止态
    NEW = enum.auto()
    READY = enum.auto()
    RUNNING = enum.auto()
    BLOCKED = enum.auto()
    TERMINATED = enum.auto()


print(Status.NEW.value)
print(Status.TERMINATED.value)

# print(re.findall(r'(\n)|(\")', r'\"\n'))
# print(re.search('\\\\', '\\'))
# print(re.search(r'\\', '\\'))
# print(r'\n')
# print('\\')

ns = SimpleNamespace(name="zsh",age="24")
print(ns)
print(vars(ns))
print(dir(ns))