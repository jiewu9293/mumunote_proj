import logging

from flask import Blueprint, render_template,request

from app.config.config import config
from app.settings import env
from model.article import Article

index = Blueprint("index",__name__)

label_types = {
    "recommend":{"name":"推荐","selected":"selected"},
    "auto_test":{"name":"自动化测试","selected":"no-selected"},
    "python":{"name":"Python","selected":"no-selected"},
    "java":{"name":"Java","selected":"no-selected"},
    "function_test":{"name":"功能测试","selected":"no-selected"},
    "perf_test":{"name":"性能测试","selected":"no-selected"},
    "funny":{"name":"幽默段子","selected":"no-selected"},
}
@index.route("/")
def home():
    page = request.args.get("page")
    article_type = request.args.get("article_type")
    logging.debug("page:" + str(page))
    logging.debug("article_type:" + str(article_type))

    if page is None:
        page = 1
    if article_type is None:
        article_type = "recommend"
    #     到数据库中查询文章数据，然后返回给前端页面
    article = Article()
    db_result = article.find_article(page, article_type)
    for article, nickname in db_result:
        article.label = label_types.get(article.label_name).get("name")

        article.create_time = str(article.create_time.month) + '.' + str(article.create_time.day)

        article.article_image = config[env].article_header_image_path + str(article.article_image)

    return render_template("index.html",result=db_result)


