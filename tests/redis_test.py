"""
requirement.txt
    redis==3.

Redis
    conn.sadd
        self.execute_command('SADD', name, *values)
            返回值类型：int
            返回值取值：0|1
    conn.zincrby
    conn.hincrby
    conn.zscore
    conn.incr

"""
import collections
import time

from redis import StrictRedis as Redis

from redis_pair_key import (
    rds_time,
    rds_score,
    rds_article,
    rds_group__article_id,
    rds_article__article_id,
    rds_voted__article_id
)


class Chapter01:
    ONE_WEEK_IN_SECONDS = 7 * 24 * 60 * 60
    VOTE_SCORE = 432
    ARTICLES_PER_PAGE = 25

    # class RedisDS:
    #     """
    #         收集 redis 的数据结构的键名，可以理解成 MySQL 的表名之类的
    #         但是这样好像也不是特别方便吧？
    #     """
    # 
    #     @staticmethod
    #     def voted__article_id(article_id):
    #         return ":".join(["voted", str(article_id)])
    # 
    #     @staticmethod
    #     def article__article_id(article_id):
    #         return ":".join(["article", str(article_id)])
    # 
    #     @staticmethod
    #     def group__article_id(article_id):
    #         return ":".join(["group", str(article_id)])
    # 
    #     @staticmethod
    #     def score():
    #         return "score:"
    # 
    #     @staticmethod
    #     def time():
    #         return "time:"
    # 
    #     @staticmethod
    #     def article():
    #         return "article:"

    def __init__(self, connect: Redis):
        self.connect = connect

    @staticmethod
    def _get_article_id(article_key: str) -> str:
        return article_key.partition(":")[-1]

    def _check_cutoff(self, article):
        cutoff = time.time() - self.ONE_WEEK_IN_SECONDS
        # 规定一篇文章发布期满一周之后，用户将不能再对它进行投票
        if self.connect.zscore(rds_score(), article) < cutoff:
            return True
        return False

    def article_vote(self, user: str, article: str, reverse=False):
        if self._check_cutoff(article):
            return

        article_id = self._get_article_id(article)
        # Redis: 向数据库中添加 <voted:{article_id}, {user}> 键值对
        if self.connect.sadd(rds_voted__article_id(article_id), user):
            # Redis: 增加 键为 score: 的 zset 类型中的 {article} 元素的分数值
            self.connect.zincrby(rds_score(),
                                 self.VOTE_SCORE if not reverse else -self.VOTE_SCORE,
                                 article)
            # Redis: 增加 键为 {article} 的 hash 类型中的以 votes 为键的键值对的值
            self.connect.hincrby(article, "votes", 1 if not reverse else -1)

    def article_negative_vote(self, user: str, article: str):
        """ 实现投反对票 """
        return self.article_vote(user, article, reverse=True)

    def post_article(self, user: str, title: str, link: str) -> str:
        # Redis: 如果以 article: 为键的键值对不存在，则创建并初始化为 1。如果存在则加一。
        #   conn.incr 在 python 中的返回值是 int 类型
        article_id = str(self.connect.incr(rds_article()))

        voted__article_id = rds_voted__article_id(article_id)
        article__article_id = rds_article__article_id(article_id)

        self.connect.sadd(voted__article_id, user)
        # 一周后删除投票用户的记录，因为一周后会冻结投票，显然不必留存了
        self.connect.expire(voted__article_id, self.ONE_WEEK_IN_SECONDS)

        now_time_stamp = time.time()
        # Redis: 此处是 python 封装的接口，设置 <{article_key}, hash> 键值对
        self.connect.hmset(article__article_id, {
            "title": title,
            "link": link,
            "poster": user,
            "time": now_time_stamp,
            "votes": 1  # 默认票数为 1
        })

        self.connect.zadd(rds_score(), {article__article_id: now_time_stamp + self.VOTE_SCORE})
        self.connect.zadd(rds_time(), {article__article_id: now_time_stamp})

        return article_id

    def get_articles(self, page, order=None):
        """ 分页返回功能 """
        if order is None:
            order = rds_score()
        start = (page - 1) * self.ARTICLES_PER_PAGE
        end = start + self.ARTICLES_PER_PAGE - 1

        # Redis: 以 {order} 为键的键值对的值（zset 类型）的反向切片 [start, end]
        ids = self.connect.zrevrange(order, start, end)
        articles = []
        for article_id in ids:
            article_data = self.connect.hgetall(article_id)
            # 添加字段
            article_data["id"] = article_id
            articles.append(article_data)
        return articles

    def add_remove_groups(self, article_id, to_add=(), to_remove=()):
        """ 将文章添加到它所在的群组 或 从群组里面移除文章 """
        article__article_id = rds_article__article_id(article_id)

        for e in to_add:
            self.connect.sadd(rds_group__article_id(e), article__article_id)
        for e in to_remove:
            self.connect.srem(rds_group__article_id(e), article__article_id)

    def get_group_articles(self, group, page, order=None):
        if order is None:
            order = rds_score()
        key = order + group
        if not self.connect.exists(key):
            # Redis: 两个集合取交集，生成一个新集合，取交集的一个集合是 zset 类型
            self.connect.zinterstore(key, [f"group:{group}", order], aggregate="max")
            self.connect.expire(key, 60)
        return self.get_articles(page, key)


class Chapter02:

    def __init__(self, connect: Redis):
        self.connect = connect

    def update_token(self, token, user, viewed_item=None):
        timestamp = time.time()
        self.connect.hset("login:", token, user)  # <token,user>
        self.connect.zadd("recent:", {token: timestamp})
        if viewed_item:
            self.connect.zadd(f"viewed:{token}", {viewed_item: timestamp})
            # 最近浏览过的 25 个商品
            self.connect.zremrangebyrank(f"viewed:{token}", 0, -26)


if __name__ == '__main__':
    conn = Redis(host="127.0.0.1", port=6379, db=0)
    # c01 = Chapter01(conn)
    # 此处可以移入类的测试函数中，此外类似 django 的测试，我这边测试结束也应该试着将旧数据删除，也就是回滚数据库
    # c01.post_article(**dict(user="张世豪", title="test4", link="https://test4"))
    # c01.post_article(**dict(user="张世豪", title="test5", link="https://test5"))

    # pipe = conn.pipeline()
    # pipe.delete("trans:")
    # pipe.incr("trans:")
    # print(pipe.get("trans:"))
    # pipe.incr("trans:", -1)
    # print(pipe.execute())

    conn.hmset("item:1", {
        "name": "物品1",
        "price": 100.01,
        "produced_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    })
    conn.hmset("item:1:seller", {
        "name": "张世豪"
    })
