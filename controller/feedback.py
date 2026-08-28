import json
import logging
import time
from flask import Blueprint, render_template, request, session, make_response, jsonify

from common import response_message
from common.utils import compress_image, model_to_json
from config.ue_config import FEEDBACK_UECONFIG

from model.favorite import Favorite
from model.feedback import Feedback

feedback = Blueprint("feedback",__name__)


@feedback.before_request
def before_comment():
    if session.get("is_login") is None or session.get("is_login") !='true':
        return {"status":9999,"data":"您好，请登录"}
    
@feedback.route("/feedback",methods=["get","post"])
def ueditor():
    param = request.args.get("action")
    print(param)
    if request.method=="GET" and param == "config":
        return make_response(FEEDBACK_UECONFIG)
    elif param == "image":
        f = request.files.get("file")
        filename = f.filename
        # 文件的后缀名
        suffix = filename.split(".")[-1]
        newname = time.strftime("%Y%m%d_%H%M%S." + suffix)
        f.save("resource/upload/" + newname)
        # 大图片压缩
        source = dest = "resource/upload" + newname
        compress_image(source, dest, 1200)

        # 构造响应数据
        result = {}
        result["state"] = "SUCCESS"
        result['url'] = "/upload/" + newname
        result["title"] = filename
        result["original"] = filename
        return jsonify(result)

# 添加一个评论
@feedback.route("/feedback/add",methods=['post'])
def add():
    #请求体 转字典
    request_data = json.loads(request.data)
    article_id = request_data.get("article_id")
    content = request_data.get("content").strip()
    #当前发表评论的人从哪个 IP 地址访问
    ipaddr = request.remote_addr
    user_id = session.get("user_id")

    # 对内容进行校验
    if len(content) < 5 or len(content) > 1000:
        return response_message.FeedbackMessage.other("内容长度不符")

    feedback = Feedback()
    try:
        result = feedback.insert_comment(user_id=user_id,
                                         article_id=article_id,
                                         content=content,
                                         ipaddr=ipaddr)
        result = model_to_json(result)
        return response_message.FeedbackMessage.success("评论成功")
    except Exception as e:
        print(e)
        return response_message.FeedbackMessage.error("评论失败")

@feedback.route("/feedback/reply",methods=['post'])
def reply():
    request_data = json.loads(request.data)
    article_id = request_data.get("article_id")
    content = request_data.get("content").strip()
    # 当前发表评论的人从哪个 IP 地址访问
    ipaddr = request.remote_addr
    user_id = session.get("user_id")
    reply_id = request_data.get("reply_id")
    base_reply_id = request_data.get("base_reply_id")

    # 对内容进行校验
    if len(content) < 5 or len(content) > 1000:
        return response_message.FeedbackMessage.other("内容长度不符")

    feedback = Feedback()
    try:
        result = feedback.insert_relpy(user_id=user_id,
                            article_id=article_id,
                            content=content,
                            ipaddr=ipaddr,
                            reply_id=reply_id,
                            base_reply_id=base_reply_id)

        return response_message.FeedbackMessage.success("评论成功")
    except Exception as e:
        print(e)
        return response_message.FeedbackMessage.error("评论失败")
