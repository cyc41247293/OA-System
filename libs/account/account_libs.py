#coding=utf-8
import json
from random import choice
from string import  printable
from datetime import datetime
from uuid import uuid4
import traceback

from libs.common.send_email.send_email_libs import send_qq_html_email

def edit_profile(self, name, password):
    if password == "":
        return {'status':False, 'msg':"密码不能为空"}

    if name == "":
        return {'status':False, 'msg':"姓名不能为空"}


    user = self.current_user
    user.name = name
    user.password = password
    user.update_time = datetime.now()
    self.db.add(user)
    self.db.commit()
    self.session.set('user_name', user.name)
    return {'status': True, 'msg': "修改成功"}



def send_email_libs(self, email):
    if email == "":
        return {'status': False, 'msg': "邮箱不能为空"}

    email_code = ''.join([choice(printable[:62]) for i in xrange(4)])

    u = str(uuid4())

    text_dict = {
        u: self.current_user.id,
        'email_code': email_code
    }

    redis_dict = json.dumps(text_dict)

    self.conn.setex('email:%s' % email, redis_dict, 500)

    content = """
        <p>html 邮件<p>
        <p><a href="http://192.168.10.128:9000/account/auth_email_code?code={}&email={}&user_id={}">点击绑定邮箱</a></p>
    
    """.format(email_code, email, u)

    send_qq_html_email("1765785706@qq.com", [email], "第一课", content)

    return {'status':True, 'msg':"邮箱发送成功"}



def auth_email_libs(self, email_code, email, u):

    redis_text = self.conn.get('email:%s' % email)
    if redis_text:
        text_dict = json.loads(redis_text)

        if text_dict and text_dict['email_code'] == email_code:
            user = self.current_user
            if not user:
                user = user.by_id(text_dict[u])

            user.email = email
            user.update_time = datetime.now()
            self.db.add(user)
            self.db.commit()
            return {'status': True, 'msg':"邮箱修改成功"}
        return {'status': False, 'msg': "邮箱验证码不正确"}
    return {'status': False, 'msg': "邮箱验证码已过期，请重新绑定"}


def add_avatar_lib(self, body):
    try:
        user = self.current_user
        user.avatar = body
        user.update_time = datetime.now()
        self.db.add(user)
        self.db.commit()
        return {'status':True}
    except Exception as e:
        print '--------'
        print traceback.format_exc()
        print '--------'
        return {'status': False, 'msg': 'error'}






