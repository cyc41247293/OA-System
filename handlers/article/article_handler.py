

import json
from handlers.base.base_handler import BaseHandler
from libs.article import article_libs

class ArticleListHandler(BaseHandler):
    def get(self):
        articles, comments, categorys, tags = article_libs.article_list_lib(self)
        kw = {
            'articles': articles,
            'newarticles': articles[:3],
            'newcomments': comments[:3],
            'categorys': categorys,
            'tags': tags,
        }
        self.render('article/article_list.html', **kw)


class AddArticleHandler(BaseHandler):
    def get(self):
        tags, categorys = article_libs.get_tags_categorys_lib(self)
        kw = {'tags':tags, 'categorys': categorys}
        self.render('article/add_article.html', **kw)

    def post(self):
        title = self.get_argument('title', '')
        article = self.get_argument('article', '')
        desc = self.get_argument('desc', '')
        category = self.get_argument('category', '')
        thumbnail = self.get_argument('thumbnail', '')
        tags = json.loads(self.get_argument('tags', ''))

        article_id = self.get_argument('article_id', '')

        print title,article, desc, category, thumbnail, tags

        result = article_libs.add_article_lib(self, title,article, desc, category, thumbnail, tags, article_id)
        if result['status'] is True:
            return self.write({'status':200, 'msg':result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class ArticleHandler(BaseHandler):
    def get(self):
        article_id = self.get_argument('id', '')
        article, comments = article_libs.article_lib(self, article_id)
        kw = {'article': article, 'comments': comments}
        self.render('article/article.html', **kw)




class AddCommentHandler(BaseHandler):
    def post(self):
        content = self.get_argument('content', '')
        article_id = self.get_argument('id', '')

        result = article_libs.add_comment_lib(self, content, article_id)
        if result['status'] is True:
            return self.write({'status':200, 'msg':result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class AddSecondCommentHandler(BaseHandler):
    def post(self):
        content = self.get_argument('content', '')
        commont_id = self.get_argument('id', '')

        result = article_libs.add_second_comment_lib(self, content, commont_id)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})




class AddLikeHandler(BaseHandler):
    def post(self):

        article_id = self.get_argument('article_id', '')

        result = article_libs.add_like_lib(self, article_id)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class ArtilceModifyManageHandler(BaseHandler):
    def get(self):
        articles = article_libs.articles_modify_list_lib()
        kw = {'articles': articles}
        self.render('article/article_modify_manage.html', **kw)



class ArtilceModifyHandler(BaseHandler):
    def get(self):
        article_id = self.get_argument('id', '')

        article, categorys, tags = article_libs.get_article_tags_categorys_lib(self, article_id)
        kw = {'article': article, 'tags': tags, 'categorys': categorys}
        self.render('article/article_modify.html', **kw)



class ArticleDeleteHandler(BaseHandler):
    def get(self):
        article_id = self.get_argument('id', '')
        articles = article_libs.article_delete_lib(self, article_id)
        kw = {'articles': articles}
        self.render('article/article_modify_manage.html', **kw)



class AddHandler(BaseHandler):
    def get(self):
        tags, categorys= article_libs.add_tags_categorys_lib(self)
        kw = {'tags': tags, 'categorys': categorys}
        return self.render('article/article_add_category_tag.html',**kw)

    def post(self):
        category_name = self.get_argument('category_name', '')
        tag_name = self.get_argument('tag_name', '')
        result = article_libs.add_categorys_tag_lib(self, category_name, tag_name)
        if result['status'] is True:
            return self.write({'status':200, 'msg':result['msg']})
        return self.write({'status':400, 'msg':result['msg']})



class SearchHandler(BaseHandler):
    def get(self):
        category_id = self.get_argument('category_id', '')
        tag_id = self.get_argument('tag_id', '')

        articles, comments, categorys, tags = article_libs.article_search_lib(self, category_id,tag_id)
        kw = {
            'articles': articles,
            'newarticles': articles[:3],
            'newcomments': comments[:3],
            'categorys': categorys,
            'tags': tags,
        }
        self.render('article/article_list.html', **kw)









