#coding=utf-8

from models.article.article_model import (
    Article, ArticleToTag, UserLikeArticle, Category,Comment,SecondComment, Tag
)


def article_list_lib(self):
    articles = Article.all_createtime_desc()
    comments = Comment.all_createtime_desc()
    tags, categorys = get_tags_categorys_lib(self)

    return articles, comments, categorys, tags

def get_tags_categorys_lib(self):
    tags = Tag.all()
    categorys = Category.all()
    return tags, categorys

def add_article_lib(self, title, content, desc, category_id, thumbnail, tags, article_id):
    if category_id == '' or tags == '':
        return {'status':False, 'msg':'请选择分类或者标签'}

    if title == '' or content=='' or desc == '':
        return {'status': False, 'msg': '请输入标题，内容， 简介'}

    if article_id != '' :
        article = Article.by_id(article_id)
        article.tags = []

    else:
        article = Article()
    article.content = content
    article.title = title
    article.desc = desc
    article.category_id = category_id
    article.thumbnail = thumbnail

    for tags_id in tags:
        tag = Tag.by_id(tags_id)
        article.tags.append(tag)

    article.user_id = self.current_user.id
    self.db.add(article)
    self.db.commit()
    if article_id != '':
        return {'status': True, 'msg': '文档修改成功'}
    return {'status': True, 'msg': '文档提交成功'}



def article_lib(self, article_id):
    article = Article.by_id(article_id)
    comments = article.comments
    return article, comments



def add_comment_lib(self, content, article_id):

    article = Article.by_id(article_id)
    if article is None:
        return {'status':False, 'msg':'文章不存在'}

    comment = Comment()
    comment.content = content
    comment.article_id = article.id
    comment.user_id = self.current_user.id
    self.db.add(comment)
    self.db.commit()
    return {'status': True, 'msg': '评论成功'}


def add_second_comment_lib(self, content, comment_id):

    comment = Comment.by_id(comment_id)
    if comment is None:
        return {'status': False, 'msg': '评论不存在'}

    second_comment = SecondComment()
    second_comment.content = content
    second_comment.comment_id = comment.id
    second_comment.user_id = self.current_user.id
    self.db.add(second_comment)
    self.db.commit()
    return {'status': True, 'msg': '二级评论成功'}

def add_like_lib(self, article_id):

    if article_id is None:
        return {'status': False, 'msg': '请输入文章ID'}

    article = Article.by_id(article_id)
    if article is None:
        return {'status': False, 'msg': '文章不存在'}

    if self.current_user in article.user_likes:
        article.user_likes.remove(self.current_user)
        self.db.add(article)
        self.db.commit()
        return {'status': True, 'msg': '取消点赞了'}


    article.user_likes.append(self.current_user)
    self.db.add(article)
    self.db.commit()
    return {'status': True, 'msg': '点赞成功'}



def articles_modify_list_lib():
    articles = Article.all()
    return articles



def get_article_tags_categorys_lib(self, article_id):
    article = Article.by_id(article_id)
    tags, categorys = get_tags_categorys_lib(self)
    return article, tags, categorys



def article_delete_lib(self, article_id):
    article = Article.by_id(article_id)
    if article is None:
        return Article.all()

    self.db.delete(article)
    self.db.commit()
    return Article.all()



def add_tags_categorys_lib(self):
    tags, categorys = get_tags_categorys_lib(self)
    return tags, categorys

def add_categorys_tag_lib(self, category_name, tag_name):
    if category_name != '':
        category = Category.by_name(category_name)
        if category is not None:
            return {'status':False, 'msg':'分类已经存在'}
        else:
            category = Category()
        category.name = category_name
        self.db.add(category)
        self.db.commit()
        return {'status': True, 'msg': '分类添加成功'}

    if tag_name != '':
        tag =Tag.by_name(tag_name)
        if tag is not None:
            return {'status': False, 'msg': '标签已经存在'}
        else:
            tag = Tag()
        tag.name = tag_name
        self.db.add(tag)
        self.db.commit()
        return {'status': True, 'msg': '标签添加成功'}

    return {'status':False, 'msg':'请输入分类或标签'}

def article_search_lib(self, category_id, tag_id):
    if tag_id != '':
        tag = Tag.by_id(tag_id)
        articles = tag.articles
    if category_id != '':
        category = Category.by_id(category_id)
        articles = category.articles

    tags, categorys = get_tags_categorys_lib(self)
    comments = Comment.all_createtime_desc()
    return articles, comments, categorys, tags