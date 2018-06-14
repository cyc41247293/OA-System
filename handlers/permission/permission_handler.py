#coding=utf-8
from handlers.base.base_handler import BaseHandler
from libs.permission import permission_libs
from libs.permission.permission_auth.permission_interface_libs import handler_permission


class ManageHandler(BaseHandler):
    def get(self):
        roles, permissions, menus, handlers, users = permission_libs.permission_manager_list_lib(self)
        kw = {
            'roles': roles,
            'permissions': permissions,
            'menus': menus,
            'handlers': handlers,
            'users': users,
            'dev_users': [],

        }
        return self.render('permission/permission_list.html', **kw)


class AddRoleHandler(BaseHandler):
    def post(self):
        name = self.get_argument('name', '')
        permission_libs.add_role_lib(self, name)
        self.redirect('/permission/manage_list')


class DelRoleHandler(BaseHandler):
    """03删除角色"""

    @handler_permission('DelRoleHandler', 'handler')
    def get(self):
        roleid = self.get_argument('id', '')
        permission_libs.del_role_lib(self, roleid)
        self.redirect('/permission/manage_list')


class AddPermissionHandler(BaseHandler):
    def post(self):
        name = self.get_argument('name', '')
        strcode = self.get_argument('strcode', '')
        permission_libs.add_permission_lib(self, name, strcode)
        self.redirect('/permission/manage_list')


class AddMenuHandler(BaseHandler):
    def post(self):
        name = self.get_argument('name', '')
        permissionid = self.get_argument('permissionid', '')
        permission_libs.add_menu_lib(self, name, permissionid)
        self.redirect('/permission/manage_list')


class DelMenuHandler(BaseHandler):
    def get(self):
        menuid = self.get_argument('menuid', '')
        permission_libs.del_menu_lib(self, menuid)
        self.redirect('/permission/manage_list')


class AddHandlerHandler(BaseHandler):
    def post(self):
        name = self.get_argument('name', '')
        permissionid = self.get_argument('permissionid', '')
        permission_libs.add_handler_lib(self, name, permissionid)
        self.redirect('/permission/manage_list')


class AddUserRoleHandler(BaseHandler):
    def post(self):
        userid = self.get_argument('userid', '')
        roleid = self.get_argument('roleid', '')
        permission_libs.add_user_role_lib(self, userid, roleid)
        self.redirect('/permission/manage_list')



class AddRolePermissionHandler(BaseHandler):
    def post(self):
        permissionid = self.get_argument('permissionid', '')
        roleid = self.get_argument('roleid', '')
        permission_libs.add_role_permission_lib(self, permissionid, roleid)
        self.redirect('/permission/manage_list')



class DelUserRoleHandler(BaseHandler):
    def get(self):
        userid = self.get_argument('userid', '')
        roleid = self.get_argument('roleid', '')
        permission_libs.del_user_role_lib(self, userid, roleid)
        self.redirect('/permission/manage_list')

