import re

from flask import Blueprint,request,make_response,session

from common import response_message
from common.email_utils import get_email_code, send_email
from common.utils import ImageCode

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
    email = request.form.get("email")

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