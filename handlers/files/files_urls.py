#coding=utf-8

import files_handler


files_urls = [
    (r'/files/files_list/(\d{1,3})', files_handler.FilesListHandler),
    (r'/files/files_upload', files_handler.FilesUploadHandler),
    (r'/files/files_down', files_handler.FilesDownLoadHandler),

    (r'/files/files_message', files_handler.FilesMessageHandler),
    (r'/files/files_page_list/(\d{1,2})', files_handler.FilesPageListHandler), # 1 10 100 999 99 3 9999

    # (r'/files/files_upload', files_handler.FilesUploadQiniuHandler),#上传七牛
    # (r'/files/files_down', files_handler.FilesDownLoadQiniuHandler), #七牛



    (r'/files/files_delete', files_handler.FilesDeleteHandler),
    (r'/files/files_recovery', files_handler.FilesRecoveryHandler),
    (r'/files/files_delete_final', files_handler.FilesDeleteFinalHandler),

    # 分享链接接口
    (r'/files/files_create_sharing_links', files_handler.FilesCreateSharingLinks),  # 创建分享链接
    (r'/files/files_auth_sharing_links', files_handler.FilesAuthSharingLinks),  # 验证分享链接
    (r'/files/files_sharing_list', files_handler.FilesSharingListHandler),  # 分享链接的文件列表
    (r'/files/files_save_sharing_links', files_handler.FilesSaveSharingHandler),  # 保存分享链接的文件



]





