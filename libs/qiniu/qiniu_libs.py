
from qiniu import Auth, put_data

access_key ='mhQj0QrtJ-APGgkVzd---zLYm3s_9OhIwOdLtiEC'
secret_key ='BcjyMsjqG4XMfNuyNqxhRCFn8oBBXX5DAdT7hijo'
bucket_name ='rock1'
q = Auth(access_key, secret_key)

def upload_qiniu_file_content(content):

    token = q.upload_token(bucket_name)

    ret, info = put_data(token, None, content)
    return ret['key'], info


def down_qiniu_file(qiniu_url):
    url = q.private_download_url(qiniu_url, expires=10)
    return url