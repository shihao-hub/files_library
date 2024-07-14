def overload_decorator(*signatures):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for sig_func in signatures:
                if all(isinstance(arg, sig_arg_type) for arg, sig_arg_type in zip(args, sig_func)):
                    return sig_func(*args, **kwargs)
            raise TypeError("No matching signature found.")

        return wrapper

    return decorator


@overload_decorator
def process(value):
    """默认处理逻辑"""
    print(f"默认处理: {value}")


@overload_decorator((int,))
def process(value: int):
    """处理整数类型"""
    print(f"处理整数: {value * 2}")


@overload_decorator((str,))
def process(value: str):
    """处理字符串类型"""
    print(f"处理字符串: {value.upper()}")


# 示例调用
process(10)  # 输出: 处理整数: 20
process("hello")  # 输出: 处理字符串: HELLO


def test_multipledispatch():
    from multipledispatch import dispatch

    @dispatch(int)
    def calculate(a):
        return a * 2

    @dispatch(int, int)
    def calculate(a, b):
        return a + b

    @dispatch(float, float)
    def calculate(a, b):
        return a * b

    @dispatch(object, object)
    def calculate(a, b):
        return f"不支持的操作: {a} 和 {b}"

    # 调用示例
    print(calculate(10))  # 输出: 20
    print(calculate(5, 3))  # 输出: 8
    print(calculate(2.5, 3.5))  # 输出: 8.75
    print(calculate("hello", 5))  # 输出: 不支持的操作: hello 和 5


test_multipledispatch()


def test_overload():
    from typing_extensions import overload

    @overload
    def calculate(a: int, b: int) -> int:
        ...

    @overload
    def calculate(a: float, b: float) -> float:
        ...

    @overload
    def calculate(a: int, b: float) -> float:
        ...

    def calculate(a, b):
        return a + b

    # 实际调用
    print(calculate(1, 2))  # 输出: 3
    print(calculate(1.5, 2.5))  # 输出: 4.0
    print(calculate())


# test_overload()

def test_singledispatch():
    from functools import singledispatch

    @singledispatch
    def add(x, y):
        raise NotImplementedError("Unsupported type")

    @add.register(int)
    @add.register(float)
    def _(x, y):
        return x + y

    @add.register(str)
    def _(x, y):
        return x + " " + y

    print(add(1, 2))  # 输出 3
    print(add(1.5, 2.5))  # 输出 4.0
    print(add("Hello", "World"))  # 输出 Hello World
# test_singledispatch()
