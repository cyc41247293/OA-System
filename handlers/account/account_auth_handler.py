#coding=utf-8
import tornado.web
from handlers.base.base_handler import BaseHandler
from libs.account import account_auth_libs

#01生成验证码
class CaptchaHandler(BaseHandler):
    def get(self):
        pre_code = self.get_argument('pre_code','')
        code = self.get_argument('code','')
        print pre_code,code
        img = account_auth_libs.create_capthca_img(self, pre_code, code)
        self.set_header("Content-Type", "image/jpg")#设置响应头
        self.write(img)

#02登录
class LoginHandler(BaseHandler):
    def get(self):
        self.render('account/auth_login.html')

    def post(self):
        name = self.get_argument('name','')
        password = self.get_argument('password','')
        code = self.get_argument('code','')
        captcha_code = self.get_argument('captcha','')

        #print name, password, code, captcha_code  #验证测试是否能获取到数据
        result = account_auth_libs.auth_captche(self, captcha_code, code)

        if result['status'] is False:
            return self.write({'status':400, 'msg':result['msg']})#write字典时，自动转换成字符串

        result = account_auth_libs.login(self, name, password)

        if result['status'] is True:#result返回状态为真
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class RegistHandler(BaseHandler):#注册
    def get(self):
        self.render('account/auth_regist.html',message='注册哈哈')
      #self.write("ok!!")
    def post(self):#from表单请求，不是ajax(ajax返回jason字符串)
        mobile = self.get_argument('mobile', '')
        mobile_captcha = self.get_argument('mobile_captcha', '')
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        captcha = self.get_argument('captcha', '')
        agree = self.get_argument('agree', '')

        result = account_auth_libs.auth_captche(self, captcha, code)

#        if result['status'] is False:
#            return self.write({'status':400, 'msg':result['msg']})#write字典时，自动转换成字符串
        #用户注册
        result = account_auth_libs.regist(self, name, mobile, mobile_captcha, password1, password2, agree)
        if result['status'] is True:
            return self.redirect('/auth/user_login')
        return self.render('account/auth_regist.html', message = 'result[msg]')

class MobileCodeHandler(BaseHandler):#接收手机短信验证码请求
    def post(self):
        mobile = self.get_argument('mobile','')
        code = self.get_argument('code','')
        captcha = self.get_argument('captcha','')

        print mobile,code,captcha   #测试后台是否取到值

        result = account_auth_libs.auth_captche(self, captcha, code)

#       if result['status'] is False:
#           return self.write({'status':400, 'msg':result['msg']})#write字典时，自动转换成字符串

        result = account_auth_libs.get_mobile_code_lib(self, mobile)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})