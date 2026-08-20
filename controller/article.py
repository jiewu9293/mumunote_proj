import logging

from flask import Blueprint, render_template,request

from app.config.config import config
from app.settings import env
from model.article import Article
from model.user import User

article = Blueprint("article",__name__)

@article.route("/detail")
def article_detail():
    article_id = request.args.get("article_id")
    article = Article()

    article_content = article.get_article_detail(article_id)
    article_tag_string = article_content.article_tag
    article_tag_list = article_tag_string.split(",")
    # 获取文章作者信息
    user = User()
    user_info = user.find_by_userid(article_content.user_id)

    # 相关文章的功能
    about_article = article.find_about_article(article_content.label_name)

    is_favorite = 1
    return render_template("article_info.html",article_content=article_content,
                           user_info=user_info,is_favorite=is_favorite,
                           article_tag_list=article_tag_list,about_article=about_article)