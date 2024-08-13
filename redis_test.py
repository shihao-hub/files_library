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

PairsNamedTuple = collections.namedtuple("PairsNamedTuple", [
    "score_pair_key",
    "time_pair_key",
    "voted_pair_key",
    "article_pair_key",
])


class Chapter01:
    # 多余...
    # PAIRS = PairsNamedTuple(*[
    #     "score:",
    #     "time:",
    #     "voted:",
    #     "article:",
    # ])

    # const
    ONE_WEEK_IN_SECONDS = 7 * 24 * 60 * 60
    VOTE_SCORE = 432
    ARTICLES_PER_PAGE = 25

    def __init__(self, connect: Redis):
        self.connect = connect

    @classmethod
    def _get_article_id(cls, article_key: str) -> str:
        return article_key.partition(":")[-1]

    def _check_cutoff(self, article):
        cutoff = time.time() - self.ONE_WEEK_IN_SECONDS
        # 规定一篇文章发布期满一周之后，用户将不能再对它进行投票
        if self.connect.zscore("score:", article) < cutoff:
            return True
        return False

    def article_vote(self, user: str, article: str, reverse=False):
        if self._check_cutoff(article):
            return

        article_id = self._get_article_id(article)
        # Redis: 向数据库中添加 <voted:{article_id}, {user}> 键值对
        if self.connect.sadd(f"voted:{article_id}", user):
            # Redis: 增加 键为 score: 的 zset 类型中的 {article} 元素的分数值
            self.connect.zincrby("score:",
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
        article_id = str(self.connect.incr("article:"))

        voted_key = f"voted:{article_id}"
        self.connect.sadd(voted_key, user)
        # 一周后删除投票用户的记录，因为一周后会冻结投票，显然不必留存了
        self.connect.expire(voted_key, self.ONE_WEEK_IN_SECONDS)

        now_time_stamp = time.time()
        article_key = f"article:{article_id}"
        # Redis: 此处是 python 封装的接口，设置 <{article_key}, hash> 键值对
        self.connect.hmset(article_key, {
            "title": title,
            "link": link,
            "poster": user,
            "time": now_time_stamp,
            "votes": 1  # 默认票数为 1
        })

        self.connect.zadd("score:", {article_key: now_time_stamp + self.VOTE_SCORE})
        self.connect.zadd("time:", {article_key: now_time_stamp})

        return article_id

    def get_articles(self, page, order="score:"):
        """ 分页返回功能 """
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
        article_key = f"article:{article_id}"
        for e in to_add:
            self.connect.sadd(f"group:{e}", article_key)
        for e in to_remove:
            self.connect.srem(f"group:{e}", article_key)

    def get_group_articles(self, group, page, order="score:"):
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
    c01 = Chapter01(Redis(host="127.0.0.1", port=6379, db=0))
    # 此处可以移入类的测试函数中，此外类似 django 的测试，我这边测试结束也应该试着将旧数据删除，也就是回滚数据库
    c01.post_article(**dict(user="张世豪", title="test4", link="https://test4"))
    c01.post_article(**dict(user="张世豪", title="test5", link="https://test5"))




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
import pprint
import time

from redis import StrictRedis as Redis

PairsNamedTuple = collections.namedtuple("PairsNamedTuple", [
    "score_pair_key",
    "time_pair_key",
    "voted_pair_key",
    "article_pair_key",
])


class Chapter01:
    """ 数据结构

        # 92617 号文章信息（行）
        article:92617 -> hash
            title, link, poster, time, votes
        # 根据发布时间排序文章的有序集合
        time: -> zset
            article - time
        # 根据评分排序文章的有序集合
        score: -> zset
            article - score
        # 为 100408 号文章投过票的用户
        voted:100408 -> set


    """
    ONE_WEEK_IN_SECONDS = 7 * 24 * 60 * 60
    VOTE_SCORE = 432
    ARTICLES_PER_PAGE = 25

    def __init__(self, connect: Redis):
        self.connect = connect

    def article_vote(self, user: str, article: str, reverse=False):
        """ 功能点之文章投票 """
        if self._check_cutoff(article):
            return

        article_id = self._get_article_id(article)

        if self.connect.sadd("voted:" + article_id, user):
            self.connect.zincrby("score:",
                                 article,
                                 self.VOTE_SCORE if not reverse else -self.VOTE_SCORE)
            self.connect.hincrby(article, "votes", 1 if not reverse else -1)

    def article_negative_vote(self, user: str, article: str):
        """ 功能点之文章投反对票 """
        raise NotImplementedError
        # return self.article_vote(user, article, reverse=True)

    def post_article(self, user: str, title: str, link: str) -> str:
        """ 功能点之发布文章 """
        article_id = str(self.connect.incr("article:"))  # 应该命名成 article_counter 之类的比较好

        voted = "voted:" + article_id
        self.connect.sadd(voted, user)
        # 一周后删除投票用户的记录，因为一周后会冻结投票，显然不必留存了
        self.connect.expire(voted, self.ONE_WEEK_IN_SECONDS)

        now_time_stamp = time.time()
        article = "article:" + article_id
        self.connect.hmset(article, {
            "title": title,
            "link": link,
            "poster": user,
            "time": now_time_stamp,
            "votes": 1  # 默认票数为 1
        })

        # redis==3.0.0 时，此处是类似 zadd 的，分数在前，pair_key 在后
        self.connect.zadd("score:", now_time_stamp + self.VOTE_SCORE, article)
        self.connect.zadd("time:", now_time_stamp, article)

        return article_id

    def get_articles(self, page, order="score:"):
        """ 功能点之分页 """
        start = (page - 1) * self.ARTICLES_PER_PAGE
        end = start + self.ARTICLES_PER_PAGE - 1

        ids = self.connect.zrevrange(order, start, end)
        articles = []
        for article_id in ids:
            article_data = self.connect.hgetall(article_id)
            # 添加字段：(Q)! 为什么 redis-py 取出来的都是
            article_data[b"id"] = article_id
            articles.append(article_data)
        return articles

    def add_remove_groups(self, article_id, to_add=(), to_remove=()):
        """ 将文章添加到它所在的群组 或 从群组里面移除文章 """
        article_key = "article:" + article_id
        for e in to_add:
            self.connect.sadd("group:" + e, article_key)
        for e in to_remove:
            self.connect.srem("group:" + e, article_key)

    def get_group_articles(self, group, page, order="score:"):
        key = order + group
        if not self.connect.exists(key):
            # Redis: 两个集合取交集，生成一个新集合，取交集的一个集合是 zset 类型
            self.connect.zinterstore(key, [f"group:{group}", order], aggregate="max")
            self.connect.expire(key, 60)
        return self.get_articles(page, key)

    @classmethod
    def _get_article_id(cls, article_key: str) -> str:
        return article_key.partition(":")[-1]

    def _check_cutoff(self, article):
        cutoff = time.time() - self.ONE_WEEK_IN_SECONDS
        # 规定一篇文章发布期满一周之后，用户将不能再对它进行投票
        if self.connect.zscore("score:", article) < cutoff:
            return True
        return False


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


class Chapter03:
    def __init__(self, connect: Redis):
        self.connect = connect


def test_chapter01():
    # db=0 就是用来测试的，所以每次测试前要清空
    conn = Redis(host="127.0.0.1", port=6379, db=0)
    conn.flushall()
    chapter = Chapter01(conn)

    for i in range(1, 11):
        chapter.post_article(f"user-{i}", f"title-{i}", f"link-{i}")
    for i in range(1, 11):
        chapter.article_vote(f"user:{i}", "article:1")

    print(f"第一页文章数：{len(chapter.get_articles(1))}")
    print(f"给 article:1 投票的用户：{conn.smembers('voted:1')}")


if __name__ == '__main__':
    test_chapter01()

    # test_conn = Redis(host="127.0.0.1", port=6379, db=1)

