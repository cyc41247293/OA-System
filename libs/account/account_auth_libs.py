#coding=utf-8
#import sys
#sys.path.append("/lib")
from utils.captcha.captcha import create_captcha
from models.account.account_user_model import User
from datetime import datetime
from random import randint
from libs.yun_tong_xun.yun_tong_xun_lib import sendTemplateSMS

def create_capthca_img(self, pre_code, code):
    if pre_code:
        self.conn.delete("captcha:%s" % pre_code)
    text, img = create_captcha()
    self.conn.setex("captcha:%s" % code,text.lower(), 60)#向radis设置键值对，3个参数，键，值，过期时间
    return img

def auth_captche(self, captcha_code, code):

    if captcha_code == '':
        return {'status':False, 'msg':'请输入图形验证码'} #将返回的消息封装成字典

    elif self.conn.get('captcha:%s' %code) != captcha_code.lower():

        return {'status': False, 'msg': '输入的图形验证码不正确'}
    return {"status": True, 'msg': '正确'}


#登录函数
def login(self, name, password):#重要，判断合法性尽量详细.是否为空，长度，恶意代码等
    if name == '' or password == '':
        return {'status': False, 'msg': '请输入用户名和密码'}

    user = User.by_name(name)
    if user and user.auth_password(password):#用户存在并且密码正确
        user.last_login = datetime.now() #上次登录时间
        user.loginnum += 1  #登录次数

        self.db.add(user)
        self.db.commit()

        self.session.set('user_name', user.name) #浏览器和系统之间的session,set到redis数据库
        return {'status': True, 'msg': '登录成功'}

    return {'status': False, 'msg': '用户名或密码不正确'}

def get_mobile_code_lib(self, mobile):
    if isinstance(mobile, unicode):#如果是unicode，转码utf-8
        mobile = mobile.encode('utf-8')
    mobile_code = randint(1000,9999)
    print '手机短信验证码是：',mobile_code
    self.conn.setex("mobile_code:%s" % mobile, mobile_code, 2000)

    sendTemplateSMS(mobile, [mobile_code, 30], 1)
    return {'status': True, 'msg': '验证码发送到%s'%mobile}

def regist(self, name, mobile, mobile_captcha, password1, password2, agree):
    if agree == "":
        return {'status': False, 'msg': "您没有点击同意条款"}

    if password1 != password2:
        return {'status': False, 'msg': "两次密码不相同"}

    if self.conn.get('mobile_code:%s' % mobile) != mobile_captcha:
        return {'status': False, 'msg': "短信验证码不正确"}

    user = User.by_name(name)
    if user is not None:
        return {'status': False, 'msg': "用户已经存在，请换一个名称"}

    user = User()
    user.name = name
    user.password = password2
    user.mobile = mobile
    self.db.add(user)
    self.db.commit()
    return {'status': True, 'msg': '用户注册成功'}