#coding=utf-8
from handlers.base.base_handler import BaseHandler

class ProfileHandler(BaseHandler):
    def get(self):
        self.render('account/account_profile.html', message=None)