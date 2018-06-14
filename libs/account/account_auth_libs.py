#coding=utf-8
from random import randint
from datetime import datetime
from utils.captcha.captcha import create_captcha
from models.account.account_user_model import User
from libs.yun_tong_xun.yun_tong_xun_lib import sendTemplateSMS

def create_captcha_img(self, pre_code, code):
    if pre_code:
        self.conn.delete("captcha:%s" % pre_code)
    text, img = create_captcha()
    self.conn.setex("captcha:%s" % code, text.lower(), 60 )
    return img

def auth_captche(self, captcha_code, code):
    if captcha_code == '':
        return {'status':False, 'msg': '请输入图形验证码'}

    elif self.conn.get('captcha:%s' %code) != captcha_code.lower():
        return {'status': False, 'msg': '输入的图形验证码不正确'}

    return {"status":True, 'msg':'正确'}


def login(self,  name, password):

    if name=='' or password == '': #重要
        return  {'status': False, 'msg': '请输入用户名或密码'}

    user = User.by_name(name)
    if user and user.auth_password(password):

        user.last_login = datetime.now()
        user.loginnum +=1

        self.db.add(user)
        self.db.commit()

        self.session.set('user_name', user.name)#######################
        return {'status': True, 'msg': '登录成功'}

    return {'status': False, 'msg': '用户名输入错误或者密码不正确'}


def get_mobile_code_lib(self, mobile):

    if isinstance(mobile, unicode):
        mobile = mobile.encode('utf-8')

    mobile_code = randint(1000,9999)
    print '手机短信验证码是：', mobile_code
    self.conn.setex("mobile_code:%s" % mobile, mobile_code, 2000 )

    #sendTemplateSMS(mobile, [mobile_code, 30], 1)

    return {'status': True, 'msg': '验证码发送到%s, 请查收'%mobile}



def regist(self, name, mobile, mobile_captcha, password1, password2, agree):
    if agree == "":
        return {'status':False, 'msg':"您没有点击同意条款"}

    if password1 != password2:
        return {'status': False, 'msg': "两次密码不相同"}

    if self.conn.get('mobile_code:%s' %mobile) != mobile_captcha:
        return {'status': False, 'msg': "短信验证码不正确"}

    user= User.by_name(name)
    if user is not None:
        return {'status': False, 'msg': "用户已经存在，请换一个名称"}


    user = User()
    user.name = name
    user.password = password2
    print user.password
    user.mobile = mobile
    self.db.add(user)
    self.db.commit()
    return {'status': True}


