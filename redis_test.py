"""
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

pairs = PairsNamedTuple(*[
    "score:",
    "time:",
    "voted:",
    "article:",
])

# const
ONE_WEEK_IN_SECONDS = 7 * 24 * 60 * 60
VOTE_SCORE = 432
ARTICLES_PER_PAGE = 25


def get_article_id(article_key: str) -> str:
    return article_key.partition(":")[-1]


def article_vote(conn: Redis, user: str, article: str):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    # 规定一篇文章发布期满一周之后，用户将不能再对它进行投票
    if conn.zscore(f"{pairs.score_pair_key}", article) < cutoff:
        return

    article_id = get_article_id(article)
    # Redis: 向数据库中添加 <voted:{article_id}, {user}> 键值对
    if conn.sadd(f"voted:{article_id}", user):
        # Redis: 增加 键为 score: 的 zset 类型中的 {article} 元素的分数值
        conn.zincrby(f"{pairs.score_pair_key}", article, VOTE_SCORE)
        # Redis: 增加 键为 {article} 的 hash 类型中的以 votes 为键的键值对的值
        conn.hincrby(article, "votes", 1)


def post_article(conn: Redis, user: str, title: str, link: str) -> str:
    # Redis: 如果以 article: 为键的键值对不存在，则创建并初始化为 1。如果存在则加一。
    #   conn.incr 在 python 中的返回值是 int 类型
    article_id = str(conn.incr("article:"))

    voted_key = f"voted:{article_id}"
    conn.sadd(voted_key, user)
    # 一周后删除投票用户的记录，因为一周后会冻结投票，显然不必留存了
    conn.expire(voted_key, ONE_WEEK_IN_SECONDS)

    now_time_stamp = time.time()
    article_key = f"article:{article_id}"
    # Redis: 此处是 python 封装的接口，设置 <{article_key}, hash> 键值对
    conn.hmset(article_key, {
        "title": title,
        "link": link,
        "poster": user,
        "time": now_time_stamp,
        "votes": 1  # 默认票数为 1
    })

    conn.zadd(f"{pairs.score_pair_key}", article_key, now_time_stamp + VOTE_SCORE)
    conn.zadd(f"{pairs.time_pair_key}", article_key, now_time_stamp)

    return article_id


def get_articles(conn: Redis, page, order=f"{pairs.score_pair_key}"):
    """ 分页返回功能 """
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    # Redis: 以 {order} 为键的键值对的值（zset 类型）的反向切片 [start, end] 
    ids = conn.zrevrange(order, start, end)
    articles = []
    for article_id in ids:
        article_data = conn.hgetall(article_id)
        # 添加字段
        article_data["id"] = article_id
        articles.append(article_data)
    return articles


def add_remove_groups(conn: Redis, article_id, to_add=(), to_remove=()):
    """ 将文章添加到它所在的群组 或 从群组里面移除文章 """
    article_key = f"article:{article_id}"
    for e in to_add:
        conn.sadd(f"group:{e}", article_key)
    for e in to_remove:
        conn.srem(f"group:{e}", article_key)


def get_group_articles(conn: Redis, group, page, order=f"{pairs.score_pair_key}"):
    key = order + group
    if not conn.exists(key):
        # Redis: 两个集合取交集，生成一个新集合，取交集的一个集合是 zset 类型
        conn.zinterstore(key, [f"group:{group}", order], aggregate="max")
        conn.expire(key, 60)
    return get_articles(conn, page, key)


if __name__ == '__main__':
    # conn = Redis(host="127.0.0.1", port=6379, db=0)
    # print(type(conn.incr("article:")))
    # print(conn.sadd("voted:1", 1))
    # print(conn.sadd("voted:1", 1))
    # print(type(conn.sadd("voted:1", 1)))
    # conn.zinterstore()
    pass
