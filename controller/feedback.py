import json
import logging
import time
from flask import Blueprint, render_template, request, session, make_response, jsonify

from common import response_message
from common.utils import compress_image
from config.ue_config import FEEDBACK_UECONFIG

from model.favorite import Favorite

feedback = Blueprint("feedback",__name__)

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