#coding=utf-8
from datetime import datetime

import tornado.escape
from models.permission.permission_model import Role
from handlers.base.base_handler import BaseHandler, BaseWebSocketHandler


#------------------提高部分 开始------------------
class SendMessageHandler(BaseWebSocketHandler):
    def get(self):
        kw  = {
            'system_msg': self.get_redis_json_to_dict('system'),
            'role_msg': self.get_redis_json_to_dict('role'),
            'user_msg': self.get_redis_json_to_dict('user'),
            'roles': Role.all(),
        }
        self.render('message/message_send_message.html', **kw)

    def get_redis_json_to_dict(self, target):
        msgs = self.conn.lrange('message:%s'%target, -5, -1)
        msgs.reverse()
        dict_list = []
        for m in msgs:
            massage_dict = tornado.escape.json_decode(m)
            dict_list.append(massage_dict)
        return dict_list



    def post(self):
        content = self.get_argument('content', '') #aaaaa   111
        user = self.get_argument('user', '')  # 222
        roleid = self.get_argument('roleid', '')
        send_type = self.get_argument('send_type', '') #  system user

        print content, user, send_type
        if send_type == "system":
            MessageWebHandler.send_system_message(self, content, send_type)
        if send_type == "role":
            MessageWebHandler.send_role_message(self, content, send_type,roleid)
        if send_type == "user":
            MessageWebHandler.send_user_message(self, content, send_type, user)
        self.redirect('/message/send_message')
#------------------提高部分 结束------------------






class MessageHandler(BaseHandler):
    def get(self):
        cache = self.conn.lrange('message:list001', -5, -1)
        cache.reverse()
        cache_list = []
        for ca in cache:
            massage_dict = tornado.escape.json_decode(ca)
            cache_list.append(massage_dict)

        kw = {'cache': cache_list}
        self.render('message/message_chat.html', **kw)


class MessageWebHandler(BaseWebSocketHandler):

    users={}

    # ------------------提高部分 开始------------------
    @classmethod
    def send_system_message(cls, self, content, send_type):
        """系统"""
        target = 'system'
        redis_msg = cls.dict_to_json(self, content, send_type, target)
        self.conn.rpush('message:%s' % send_type, redis_msg)


        for f, v in MessageWebHandler.users.iteritems():
            v.write_message(redis_msg)

    @classmethod
    def dict_to_json(cls, self, content, send_type, target):
        msg = {
            "content": content,
            "send_type": send_type,
            "sender": self.current_user.name,
            "target": target,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return tornado.escape.json_encode(msg)

    @classmethod
    def send_role_message(cls, self, content, send_type, roleid):
        """角色"""
        role = Role.by_id(roleid)
        redis_msg = cls.dict_to_json(self, content, send_type, role.name)
        self.conn.rpush('message:%s' % send_type, redis_msg)
        role_users = role.users  # [zhangsan, lishi , wangwu]  [zhangsan, lishi]
        for user in role_users:
            if MessageWebHandler.users.get(user.name, None) is not None:
                MessageWebHandler.users[user.name].write_message(redis_msg)
            else:
                # self.conn.lpush("ws:role_off_line",message)
                pass

    @classmethod
    def send_user_message(cls, self, content, send_type, user):
        """个人"""
        redis_msg = cls.dict_to_json(self, content, send_type, user)

        self.conn.rpush('message:%s' % send_type, redis_msg)

        if cls.users.get(user, None) is not None:
            cls.users[user].write_message(redis_msg)
        else:
            # self.conn.lpush("ws:user_off_line",message)
            pass

    # ------------------提高部分 结束------------------




    #------------------掌握的部分 开始------------------
    def open(self):
        MessageWebHandler.users[self.current_user.name] = self
        print MessageWebHandler.users
        pass

    def on_close(self):
        pass

    def on_message(self, message):
        #{"content_html":"abc"}

        print message
        msg = tornado.escape.json_decode(message)
        msg.update({
            "name": self.current_user.name,
            "useravatar": self.current_user.avatar,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        message = tornado.escape.json_encode(msg)

        self.conn.rpush('message:list001', message)

        for f,v in MessageWebHandler.users.iteritems():
            v.write_message(message)

    #------------------掌握的部分 结束------------------

