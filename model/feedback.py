import random

from sqlalchemy import Table, func

from common.database import db_connect
from config.config import config
from model.user import User
from settings import env
from common.utils import model_to_json

db_session,Base,engine = db_connect()


class Feedback(Base):
    # 表结构的反射加载
    __table__ = Table("comment",Base.metadata,autoload_with=engine)

    def get_feedback_user_list(self,article_id):
        final_data_list = []
        #查询一级评论
        feedback_list = self.find_feedback_by_article_id(article_id)
        for feedback in feedback_list:
            user = User()
            # 根据一级评论的数据，获取回复评论的评论的内容
            all_reply = self.find_reply_by_replyid(base_reply_id=feedback.id)
            #在找：这条一级评论是谁发的。
            feedback_user = user.find_by_userid(feedback.user_id)
            #遍历一级评论的每个评论
            reply_list = []
            # 再根据每一条回复的评论，查询用户信息
            for reply in all_reply:
                # 用于存储当前这条原始评论的所有回复评论，如果没有回复，这个值就为空
                reply_content_with_user = {}
                #获取回复评论的用户信息
                from_user_data = user.find_by_userid(reply.user_id)
                #获取被回复评论的用户信息
                to_user_reply_data = self.find_reply_by_id(reply.reply_id)
                to_user_data = user.find_by_userid(to_user_reply_data[0].user_id)

                reply_content_with_user["from_user"] = model_to_json(from_user_data)
                reply_content_with_user["to_user"] = model_to_json(to_user_data)
                reply_content_with_user["content"] = model_to_json(reply)
                reply_list.append(reply_content_with_user)

            every_feedback_data = model_to_json(feedback)
            every_feedback_data.update(model_to_json(feedback_user))
            every_feedback_data["reply_list"] = reply_list
            final_data_list.append(every_feedback_data)
        return final_data_list




    def find_feedback_by_article_id(self,article_id):
       result = db_session.query(Feedback).filter_by(
            article_id=article_id,
           #一级评论的两个条件
            base_reply_id=0,
            reply_id=0,
        ).order_by(
            Feedback.id.desc()
        ).all()

       return result

    def find_reply_by_id(self, id):
        result = db_session.query(Feedback).filter(
            Feedback.id == id
        ).order_by(
            Feedback.id.desc()
        ).all()
        return result

    def find_reply_by_replyid(self, base_reply_id):
        #根据某条一级评论的 id，找到它下面所有的回复评论，并按照回复时间（id）倒序排列
        result = db_session.query(Feedback).filter_by(
            base_reply_id=base_reply_id
        ).order_by(
            Feedback.id.desc()
        ).all()
        return result

    def get_article_feedback_count(self, article_id):
        result = db_session.query(Feedback).filter_by(
            article_id=article_id,
            reply_id=0,
            base_reply_id=0
        ).count()
        return result

    # 插入一级评论
    def insert_comment(self,user_id,article_id,content,ipaddr):
        # label的意思就是重新起一个名字给字段
        feedback_max_floor = db_session.query(
            #给查询结果起一个临时名字 max_floor 方便这样 feedback_max_floor.max_floor
            func.max(Feedback.floor_number).label("max_floor")
        # 只查询当前文章的评论。
        ).filter_by(article_id=article_id).first()
        if feedback_max_floor.max_floor == 0 or feedback_max_floor.max_floor is None:
            feedback = Feedback(user_id=user_id,
                                article_id=article_id,
                                content=content,
                                ipaddr=ipaddr,
                                floor_number=1,
                                reply_id=0,
                                base_reply_id=0)
        else:
            feedback = Feedback(user_id=user_id,
                            article_id=article_id,
                            content=content,
                            ipaddr=ipaddr,
                            floor_number=int(feedback_max_floor.max_floor) + 1,
                            reply_id=0,
                            base_reply_id=0)
        db_session.add(feedback)
        db_session.commit()
        # 刚插入时有些值由数据库自动生成，refresh(feedback) 可以把这些值重新读取到 Python对象里。
        # db_session.refresh()
        return feedback

    def insert_reply(self,user_id,article_id,content,ipaddr,reply_id,base_reply_id):
        feedback = Feedback(user_id=user_id,
                            article_id=article_id,
                            content=content,
                            ipaddr=ipaddr,
                            reply_id=reply_id,
                            base_reply_id=base_reply_id)
        db_session.add(feedback)
        db_session.commit()





