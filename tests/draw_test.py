# 1. 导入相关库
import matplotlib as mpl
import matplotlib.pyplot as plt

# 2. 创建 figure 画布对象
figure = plt.figure ()
# 3. 获取对应位置的 axes 坐标系对象
axes1 = figure.add_subplot (2, 1, 1)
axes2 = figure.add_subplot (2, 1, 2)
# 4. 调用 axes 对象，进行对应位置的图形绘制
axes1.plot ([1, 3, 5, 7], [4, 9, 6, 8])
axes2.plot ([1, 2, 4, 5], [8, 4, 6, 2])
# 5. 显示图形
figure.show ()

# class MyClass:
#     def my_method(self, value):
#         print(f"Value: {value}, and this is an instance method.")
#
# # 创建一个实例
# my_instance = MyClass()
#
# # 定义一个回调函数，这里没有绑定实例
# def callback(function, value):
#     function(value)  # 这里调用时没有提供self
#
# # 将实例方法作为回调传递
# callback(my_instance.my_method, 42)  # 这里会抛出TypeError，因为my_method需要一个self参数