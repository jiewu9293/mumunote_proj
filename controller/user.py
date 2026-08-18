import re
import json
from flask import Blueprint,request,make_response,session
import hashlib
from common import response_message
from common.email_utils import get_email_code, send_email
from common.utils import ImageCode
from model.user import User

user = Blueprint("user",__name__)

@user.route("/vcode")
def vcode():
    code,bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers["Content-Type"]="image/jpeg"
    # 存储起来，我们暂时存储到内存中，也就是session里边
    session['vcode'] = code.lower()
    print(code.lower())
    return response

@user.route("/ecode",methods=["POST"])
def email_code():
    email = json.loads(request.data).get("email")

    if not re.match(".+@.+\..+", email):
        return response_message.UserMessage.other("无效的邮箱")

    code = get_email_code()

    # 发送邮件
    try:
        send_email(email, code)
        session['ecode'] = code.lower()
        return response_message.UserMessage.success("邮件发送成功")
    except Exception as e:
        print(e)
        return response_message.UserMessage.error("邮件发送失败")
    return code

@user.route("/reg",methods=["post"])
def register():
    #把前端发来的 JSON 转成 Python 字典
    request_data = json.loads(request.data)
    username=request_data.get("username")
    password=request_data.get("password")
    second_password=request_data.get("second_password")
    ecode=request_data.get("ecode")
    # 做数据的验证
    if ecode.lower() != session.get("ecode"):
        return response_message.UserMessage.error("邮箱验证码错误")
    # 用户名 和 密码的验证
    if not re.match(".+@.+\..+", username):
        return response_message.UserMessage.other("无效的邮箱")

    if len(password) < 6:
        return response_message.UserMessage.error("密码不合法")

    if password != second_password:
        return response_message.UserMessage.error("两次密码不一致")
    # 用户名是否已经注册
    user = User()
    if len(user.find_by_username(username=username)) > 0:
        return response_message.UserMessage.error("用户名已经存在")

        # 实现注册的功能了
    password = hashlib.md5(password.encode()).hexdigest()
    result = user.do_register(username=username, password=password)
    return response_message.UserMessage.success("用户注册成功")