import enum
from typing import List


class Price:
    def get_charge(self, days_rented):
        raise NotImplementedError

    def get_frequent_renter_points(self, days_rented):
        return 1


class RegularPrice(Price):
    def get_charge(self, days_rented):
        result = 2
        if days_rented > 2:
            result += (days_rented - 2) * 1.5
        return result


class NewReleasePrice(Price):
    def get_charge(self, days_rented):
        return days_rented * 3

    def get_frequent_renter_points(self, days_rented):
        return 2 if days_rented > 1 else 1


class ChildrenPrice(Price):
    def get_charge(self, days_rented):
        result = 1.5
        if days_rented > 3:
            result = (days_rented - 3) * 1.5
        return result


class Movie:
    REGULAR = 0
    NEW_RELEASE = 1
    CHILDREN = 2

    # <Q>(!)
    class Types(enum.Enum):
        REGULAR = 0
        NEW_RELEASE = 1
        CHILDREN = 2

    def __init__(self, title: str, price_code: int):
        self._title = title
        self._price_code = price_code
        self._price = self._generate_price()

    def _generate_price(self):
        price_code = self.get_price_code()
        if price_code == Movie.REGULAR:
            return RegularPrice()
        elif price_code == Movie.NEW_RELEASE:
            return NewReleasePrice()
        elif price_code == Movie.CHILDREN:
            return ChildrenPrice()
        return Price()

    def get_price_code(self):
        return self._price_code

    def set_price_code(self, price_code):
        self._price_code = price_code

    def get_title(self):
        return self._title

    def get_charge(self, days_rented):
        # 此处有分支条件的，分支可以用子类即多态取代，
        #   此处没有单纯使用 Movie 的子类，而是通过
        #   策略模式，即组合，在只改变 Movie 的情况
        #   下，实现多态取代条件逻辑的功能
        # 单纯使用 Movie 的子类的情况：
        #   RegularMovie.get_charge
        #   NewReleaseMovie.get_charge
        #   ChildrenMovie.get_charge
        #   这导致其他地方的代码需要修改，尤其 Movie 实例化的 对象
        return self._price.get_charge(days_rented)

    def get_frequent_renter_points(self, days_rented):
        # 同 get_charge 的注释
        return self._price.get_frequent_renter_points(days_rented)


class Rental:
    def __init__(self, movie: Movie, days_rented: int):
        self._movie = movie
        self._days_rented = days_rented
        self._saved_charge = None

    def get_days_rented(self):
        return self._days_rented

    def get_movie(self):
        return self._movie

    def get_charge(self):
        """ 根据不同的影片类型和租赁时间计算这个影片的费用 """
        # 减少计算次数，优化性能
        if self._saved_charge:
            return self._saved_charge

        movie, days_rented = self.get_movie(), self.get_days_rented()
        res = movie.get_charge(days_rented)

        self._saved_charge = res
        return res

    def get_frequent_renter_points(self):
        """ 计算顾客的常客积分 """
        # 这次也是重构抽出去的，抽到 Movie 类中
        movie, days_rented = self.get_movie(), self.get_days_rented()
        return movie.get_frequent_renter_points(days_rented)


class Customer:

    def __init__(self, name: str):
        self._name = name
        self._rentals: List[Rental] = []

    def add_rental(self, rental: Rental):
        self._rentals.append(rental)

    def get_name(self):
        return self._name

    def get_total_charge(self):
        res = 0.0
        for e in self._rentals:
            res += e.get_charge()
        return res

    def get_total_frequent_renter_points(self):
        res = 0
        for e in self._rentals:
            res += e.get_frequent_renter_points()
        return res

    def statement(self) -> str:
        # 用于打印结果
        res = "Rental Record for " + self.get_name() + "\n"
        for e in self._rentals:
            res += "\t" + e.get_movie().get_title() + "\t" + str(e.get_charge()) + "\n"
        res += "Amount owed is " + str(self.get_total_charge()) + "\n"
        res += "You earned " + str(self.get_total_frequent_renter_points()) + " frequent renter points"
        return res

    def html_statement(self) -> str:
        res = "<p><h1>Rental Record for <em>" + self.get_name() + "</em></h1></p>\n"
        for e in self._rentals:
            res += "\t" + e.get_movie().get_title() + "\t" + str(e.get_charge()) + "<br>\n"
        res += "<p>Amount owed is <em>" + str(self.get_total_charge()) + "</em></p>\n"
        res += ("<p>You earned <em>" + str(self.get_total_frequent_renter_points())
                + "</em> frequent renter points</p>")
        return res


if __name__ == '__main__':
    customer = Customer("张三")
    customer.add_rental(Rental(Movie("蜡笔小新1", Movie.CHILDREN), 10))
    customer.add_rental(Rental(Movie("蜡笔小新2", Movie.REGULAR), 10))
    customer.add_rental(Rental(Movie("蜡笔小新3", Movie.NEW_RELEASE), 10))
    print(customer.statement())
    # print()
    # print(customer.html_statement())


