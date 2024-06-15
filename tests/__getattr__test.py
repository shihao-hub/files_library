class Dog:
    def __getattr__(self, item):
        return "__getattr__ -> {}".format(item)


dog = Dog()

print(dog.a)