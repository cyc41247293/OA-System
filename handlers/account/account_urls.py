#coding=utf-8
import account_auth_handler
import account_handler

account_urls = [
    (r'/auth/user_login', account_auth_handler.LoginHandler),
    (r'/auth/captcha', account_auth_handler.CaptchaHandler),
    (r'/auth/user_regist', account_auth_handler.RegistHandler),
    (r'/auth/mobile_code', account_auth_handler.MobileCodeHandler), #以上为auth

    (r'/account/user_profile', account_handler.ProfileHandler),   #以下在account
]