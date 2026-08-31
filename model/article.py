from sqlalchemy import Table, or_
from app.config.config import config
from app.settings import env
from common.database import db_connect
from model.user import User

db_session,Base,engine = db_connect()


class Article(Base):
    # 表结构的反射加载
    __table__ = Table("article",Base.metadata,autoload_with=engine)

    def find_article(self,page,article_type="recommend"):
        if int(page) < 1:
            page = 1
        count = int(page) * config[env].page_count

        if article_type == "recommend":
            result = db_session.query(Article, User.nickname).join(
                User, User.user_id == Article.user_id
            ).filter(
                Article.drafted == 1
            ).order_by(
                Article.browse_num.desc()
            ).limit(count).all()
        else:
            result = db_session.query(Article, User.nickname).join(
                User, User.user_id == Article.user_id
            ).filter(
                Article.label_name == article_type,
                Article.drafted == 1
            ).order_by(
                Article.browse_num.desc()
            ).limit(count).all()
        return result

    def search_article(self, page, keyword):
        if int(page) < 1:
            page = 1
        count = int(page) * config[env].page_count
        result = db_session.query(
            Article, User.nickname).join(
            User, User.user_id == Article.user_id).filter(
            or_(Article.title.like("%" + keyword + "%"),
                Article.article_content.like("%" + keyword + "%"))
        ).order_by(
            Article.browse_num.desc()
        ).limit(count).all()
        return result

    def get_article_detail(self, article_id):
        result = db_session.query(Article).filter_by(id=article_id).first()

        result.browse_num += 1

        db_session.commit()
        return result

    # 获取相关文章的数据
    def find_about_article(self, label_name):
        return db_session.query(Article).filter_by(
            label_name=label_name).order_by(
            Article.browse_num.desc()
        ).limit(5)