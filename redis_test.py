import time

from redis import StrictRedis as Redis

# const
ONE_WEEK_IN_SECONDS = 7 * 24 * 60 * 60
VOTE_SCORE = 432


def get_article_id(article_key: str) -> str:
    return article_key.partition(":")[-1]


def article_vote(conn: Redis, user: str, article: str):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    # 规定一篇文章发布期满一周之后，用户将不能再对它进行投票
    if conn.zscore("time:", article) < cutoff:
        return

    article_id = get_article_id(article)
    if conn.sadd(f"voted:{article_id}", user):
        conn.zincrby("score:", article, VOTE_SCORE)
        conn.hincrby(article, "votes", 1)


def post_article(conn: Redis, user, title, link):
    # INCR key -> key:value, 没有就创建该键值对，有就自增值
    #   conn.incr("article:") 返回值是 int，看样子 redis 库会自动转换
    article_id = str(conn.incr("article:"))


if __name__ == '__main__':
    conn = Redis(host="127.0.0.1", port=6379, db=0)
    print(type(conn.incr("article:")))
