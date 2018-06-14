#coding=utf-8
import tornado.escape
import tornado.web
import tornado.websocket
from libs.pycket.session import SessionMixin
from libs.db.dbsession import dbSession
from libs.redis_conn.redis_conn import conn
from models.account.account_user_model import User

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):
        self.flashes = None
        self.db=dbSession #操作mysql
        self.conn = conn #操作redis


    def get_current_user(self):
        """获取当前用户"""
        username = self.session.get("user_name") #zhangsan
        user = None
        if username:
            user = User.by_name(username)
        return user if user else None

        # if user:
        #     return user
        # else:
        #     return None

    def on_finish(self):
        self.db.close()


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    def initialize(self):
        self.flashes = None
        self.db=dbSession #操作mysql
        self.conn = conn #操作redis


    def get_current_user(self):
        """获取当前用户"""
        username = self.session.get("user_name") #zhangsan
        user = None
        if username:
            user = User.by_name(username)
        return user if user else None


    def on_finish(self):
        self.db.close()