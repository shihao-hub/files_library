def rds_voted__article_id(article_id):
    return ":".join(["voted", str(article_id)])


def rds_article__article_id(article_id):
    return ":".join(["article", str(article_id)])


def rds_group__article_id(article_id):
    return ":".join(["group", str(article_id)])


def rds_score():
    return "score:"


def rds_time():
    return "time:"


def rds_article():
    return "article:"