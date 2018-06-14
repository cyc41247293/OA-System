#coding=utf-8

from handlers.base.base_handler import BaseHandler
from libs.files import files_lib
import tornado.gen
from concurrent.futures import ThreadPoolExecutor
executor_g = ThreadPoolExecutor(50)

class FilesListHandler(BaseHandler):
    def get(self, page):
        files = files_lib.files_list_lib(self)
        kw = {'files': files}
        return  self.render('files/files_list.html', **kw)


class FilesUploadHandler(BaseHandler):
    executor = executor_g

    def get(self):
        return self.render('files/files_upload.html')


    @tornado.gen.coroutine
    def post(self):
        upload_files = self.request.files.get('importfile', '')
        yield  files_lib.upload_files_lib(self, upload_files)
        self.write({'status': 200, 'msg': '保存成功'})
        # if result is None:
        #     return self.write({'status':400, 'msg': '有错误'})
        # return self.write({'status': 200, 'msg': '保存成功', 'data': result})

"""
[
    {'status': False, 'msg': '文件格式不正确', 'data':''},
    {'status': True, 'msg': '文件保存成功(其实以前有人上传过了)', 'data':file_path}
    {'status': True, 'msg': '文件保存成功', 'data': file_path}
]
"""


class FilesMessageHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        files= files_lib.files_message_lib(self, uuid)
        kw = {'files': files}
        return self.render('files/files_message.html', **kw)



class FilesPageListHandler(BaseHandler):
    def get(self, page):

        files, files_page, files_del = files_lib.file_page_lib(self, page)
        kw = {
            'files': files,
            'files_page':files_page,
            'files_del':files_del
        }
        self.render('files/files_page_list.html', **kw)



class FilesDeleteHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        files_lib.files_delete_lib(self, uuid)
        return self.redirect('/files/files_page_list/1')


class FilesRecoveryHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        files_lib.files_recovery_lib(self, uuid)
        return self.redirect('/files/files_page_list/1')


class FilesDeleteFinalHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        files_lib.files_delete_final_lib(self, uuid)
        return self.redirect('/files/files_page_list/1')


#-----------------------------分享链接处理器-------------------------------
class FilesCreateSharingLinks(BaseHandler):
    """001创建分享链接"""
    def get(self):
        uuid = self.get_argument('uuid', '')
        fileslinks, password = files_lib.create_sharing_links_lib(self, uuid)
        kw = {'fileslinks': fileslinks, 'password': password}
        self.render('files/files_create_sharing_links.html', **kw)


class FilesAuthSharingLinks(BaseHandler):
    """002使用密码验证分享链接"""
    def get(self):
        uu = self.get_argument('uuid', '')
        result = files_lib.get_username_lib(self, uu)
        if result['status'] is False:
            kw = {'username': result['username'], 'uuid1': uu, 'msg': result['msg']}
            return self.render('files/files_auth_sharing_links.html', **kw)
        kw = {'username': result['username'], 'uuid1': uu, 'msg': ''}
        self.render('files/files_auth_sharing_links.html', **kw)

    def post(self):
        uu = self.get_argument('uuid', '')
        password = self.get_argument('password', '')
        result = files_lib.get_sharing_files_lib(self, uu, password)
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        return self.write({'status': 200, 'msg': result['msg'], 'links': result['links']})


class FilesSharingListHandler(BaseHandler):
    """003查看分享的文件"""
    def get(self):
        uu = self.get_argument('uuid', '')
        print self.session.set('sharing', 'aa')
        result = files_lib.files_sharing_list_lib(self, uu)
        if result['status'] is True:
            kw = {'files': result['data'], 'uuid': result['uuid']}
            return self.render('files/files_sharing_list.html', **kw)
        return self.write(result['msg'])


class FilesSaveSharingHandler(BaseHandler):
    """004保存分享的文件"""
    def get(self):
        uu = self.get_argument('uuid', '')
        result = files_lib.save_sharing_files_lib(self, uu)
        if result['status'] is True:
            return self.redirect('/files/files_page_list/1')
        return self.write(result['msg'])

#-----------------------------分享链接处理器-------------------------------

class FilesUploadQiniuHandler(BaseHandler):
    """03文件上传到七牛服务器"""
    def get(self):
        self.render('files/files_upload.html')

    def post(self):
        upload_files =self.request.files.get('importfile', None)
        result = files_lib.upload_files_qiniu_lib(self, upload_files)
        if result is None:
            return self.write({'status': 400, 'msg': '有错误了'})
        return self.write({'status': 200, 'msg': '有错误了','data': result})


class FilesDownLoadQiniuHandler(BaseHandler):
    """04从七牛服务器下载文件"""
    def get(self):
        uuid =self.get_argument('uuid', '')
        result = files_lib.files_download_qiniu_lib(self, uuid)
        if result['status'] is True:
            return self.redirect(result['data'])
        else:
            return self.write(result['msg'])





#重点掌握
class FilesDownLoadHandler(BaseHandler):
    executor = executor_g
    @tornado.gen.coroutine
    def get(self):
        uuid = self.get_argument('uuid', '')
        yield files_lib.files_download_lib(self, uuid)


