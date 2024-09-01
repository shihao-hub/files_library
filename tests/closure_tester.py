def create_functions():
    res = []
    for i in range(10):
        def anonymous(num):
            def anonymous_ret():
                return num

            return anonymous_ret

        # res.append((lambda x: lambda: x)(i)) # 等价于下面这一行
        res.append(anonymous(i))
    return res


def output_numbers(count):
    for i in range(count):
        def block_scope():
            for j in range(100):
                pass

        block_scope()
    print(i)
    print(j)


if __name__ == '__main__':
    # for fn in create_functions():
    #     print(fn())
    output_numbers(10)
