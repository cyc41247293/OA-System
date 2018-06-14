#coding=utf-8
from models.permission.permission_model import Role, Permission, Menu, Handler
from models.account.account_user_model import User
from libs.flash.flash_lib import flash

def permission_manager_list_lib(self):

    roles = Role.all()
    permissions = Permission.all()
    menus = Menu.all()
    handlers = Handler.all()
    users = User.all()
    return roles, permissions, menus, handlers, users


def add_role_lib(self, name):

    role= Role.by_name(name)
    if role is not None:
        flash(self, "角色已经存在，添加失败", "error")
        return
    role = Role()
    role.name = name
    self.db.add(role)
    self.db.commit()
    flash(self, "角色添加成功", "success")


def del_role_lib(self, roleid):
    """03删除角色"""
    role= Role.by_id(roleid)
    if role is None:
        flash(self, "角色删除失败", "error")
        return
    self.db.delete(role)
    self.db.commit()
    flash(self, "角色删除成功", "success")


def add_permission_lib(self, name, strcode):

    permission= Permission.by_name(name)
    if permission is not None:
        return
    permission = Permission()
    permission.name = name
    permission.strcode = strcode
    self.db.add(permission)
    self.db.commit()



def add_menu_lib(self, name, permissionid):

    permission = Permission.by_id(permissionid)
    if permission is None:
        return

    menu = Menu.by_name(name)#注意
    if menu is None:
        menu = Menu()

    menu.name = name
    menu.permission = permission #问题 可不可以
    #menu.p_id = permissionid
    self.db.add(menu)
    self.db.commit()


def del_menu_lib(self, menuid):

    menu = Menu.by_id(menuid)
    if menu is None:
        return
    self.db.delete(menu)
    self.db.commit()


def add_handler_lib(self, name, permissionid):

    permission = Permission.by_id(permissionid)
    if permission is None:
        return

    hanlder = Handler.by_name(name)  # 注意
    if hanlder is None:
        hanlder = Handler()

    hanlder.name = name
    hanlder.permission = permission  # 问题 可不可以
    self.db.add(hanlder)
    self.db.commit()


def add_user_role_lib(self, userid, roleid):
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    if user is None or role is None:
        return
    user.roles.append(role) #多对多关系添加
    #role.users.append(user)

    self.db.add(user)
    self.db.commit()


def add_role_permission_lib(self, permissionid, roleid):
    permission = Permission.by_id(permissionid)
    role = Role.by_id(roleid)

    if permission is None or role is None:
        return
    permission.roles.append(role) #多对多关系添加
    self.db.add(permission)
    self.db.commit()



def del_user_role_lib(self, userid):
    user = User.by_id(userid)
    if user is None:
        return
    user.roles = []
    self.db.add(user)
    self.db.commit()













