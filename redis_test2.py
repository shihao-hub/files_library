"""
requirement.txt
    redis==2.7.0

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
from urllib.request import Request
from http.client import HTTPResponse

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
            title: "title"
            link: "link"
            poster: "poster"
            time: "time"
            votes: "votes"
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
        """ 将文章添加到它所在的群组 或 从群组里面移除文章
            to_add, to_remove 的元素形如 "article:1"
        """
        article = "article:" + article_id
        for e in to_add:
            self.connect.sadd("group:" + e, article)
        for e in to_remove:
            self.connect.srem("group:" + e, article)

    def get_group_articles(self, group, page, order="score:"):
        key = order + group
        if not self.connect.exists(key):
            # Redis: 两个集合取交集，生成一个新集合，取交集的一个集合是 zset 类型
            self.connect.zinterstore(key, [f"group:{group}", order], aggregate="max")
            self.connect.expire(key, 60)
        return self.get_articles(page, key)

    def _get_article_id(self, article_key: str) -> str:
        return article_key.partition(":")[-1]

    def _check_cutoff(self, article):
        cutoff = time.time() - self.ONE_WEEK_IN_SECONDS
        # 规定一篇文章发布期满一周之后，用户将不能再对它进行投票
        if self.connect.zscore("score:", article) < cutoff:
            return True
        return False

    @staticmethod
    def test():
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


class Chapter02:
    """
        token: 令牌

    """

    def __init__(self, connect: Redis):
        self.connect = connect
        self.QUIT = False
        self.LIMIT = 10000000

    def check_token(self, token):
        return self.connect.hget("login:", token)

    def update_token(self, token, user, viewed_item=None):
        """ 记录用户最后一次浏览商品的时间以及用户最近浏览了哪些商品
            注意，此处设置的键值与 token 绑定，因此 token 更新的时候需要将就数据全部清空
        """
        timestamp = time.time()
        self.connect.hset("login:", token, user)  # <token,user>
        self.connect.zadd("recent:", token, timestamp)  # zset 默认排序是升序排序
        if viewed_item:
            self.connect.zadd(f"viewed:{token}", viewed_item, timestamp)
            # 最近浏览过的 25 个商品
            self.connect.zremrangebyrank(f"viewed:{token}", 0, -26)

    def clean_sessions(self):
        """ 清空旧的会话数据：(N)! 该例子没办法试验

        """
        while not self.QUIT:
            size = self.connect.zcard("recent:")
            if size <= self.LIMIT:
                time.sleep(1)  # 会话数量低于 LIMIT 时，休眠一秒钟再检测
                continue

            # 每次将多余的 100 个清理掉，为什么就 100 个呢？
            #   主要是根据需求来的，本书的例子里，平均每秒来 60 个会话
            end_index = min(size - self.LIMIT, 100)
            tokens = self.connect.zrange("recent:", 0, end_index - 1)

            session_keys = []
            for token in tokens:
                session_keys.append("viewed:" + token)

            self.connect.delete(*session_keys)
            self.connect.hdel("login:", *tokens)
            self.connect.zrem("recent:", *tokens)

    def add_to_cart(self, session, item, count):
        """ 使用 cookie 实现购物车 """
        if count <= 0:
            self.connect.hdel("cart:" + session, item)
        else:
            self.connect.hset("cart:" + session, item, count)

    def clean_full_session(self):
        pass

    def cache_request(self, request: Request, callback):
        """ 网页缓存：将短时间不必重新生成的 html 页面缓存起来，个人认为 GET 一般都可以缓存 """

        expire_time = 300
        page = "cache:" + hash(request)
        content = self.connect.get(page)

        if not content:
            content = callback(request)
            self.connect.setex(page, expire_time, content)

        return content


class Chapter03:
    def __init__(self, connect: Redis):
        self.connect = connect


class Chapter05:
    PRECISION = [1, 5, 60, 300, 3600, 18000, 86400]

    def __init__(self, connect: Redis):
        self.connect = connect

    def update_counter(self, name, count=1, now=None):
        now = now or time.time()
        pipe = self.connect.pipeline()
        for precision in self.PRECISION:
            pnow = int(now / precision) * precision  # 时间片节点
            # (Q)!: 为什么每次都要生成一次？
            pipe.zadd("known:", 0, f"{precision}:{name}")
            pipe.hincrby(f"count:{precision}:{name}", pnow, count)
        pipe.execute()

    def get_counter(self, name, precision):
        count = f"count:{precision}:{name}"
        res = [(k, v) for k, v in self.connect.hgetall(count).items()]
        res.sort()
        return res

    @staticmethod
    def test():
        conn = Redis(host="127.0.0.1", port=6379, db=0)
        conn.flushall()
        chapter = Chapter05(conn)
        for i in range(10):
            print(f"point {i} (max={10})")
            chapter.update_counter("hits")
            chapter.update_counter("hits")
            chapter.update_counter("hits")
            time.sleep(1)
        print(chapter.get_counter("hits", 5))


if __name__ == '__main__':
    # Chapter01.test()
    # Chapter05.test()

    # test_conn = Redis(host="127.0.0.1", port=6379, db=1)

    conn = Redis(host="127.0.0.1", port=6379, db=0)

    # 键名模拟嵌套结构特性
    conn.flushall()
    conn.hmset("user:123", {
        "name": "张世豪",
        "age": 23
    })
    conn.rpush("user:123:relatives", *["张先柱", "张恒玲"])
