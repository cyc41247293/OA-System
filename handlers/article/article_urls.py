
import article_handler


article_urls = [
    (r'/article/article_list', article_handler.ArticleListHandler),
    (r'/article/add_article', article_handler.AddArticleHandler),
    (r'/article/article', article_handler.ArticleHandler),

    (r'/article/addcomment', article_handler.AddCommentHandler),
    (r'/article/addsecondcomment', article_handler.AddSecondCommentHandler),
    (r'/article/addlike', article_handler.AddLikeHandler),

    (r'/article/article_modify_manage', article_handler.ArtilceModifyManageHandler),

    (r'/article/article_modify', article_handler.ArtilceModifyHandler),

    (r'/article/article_delete', article_handler.ArticleDeleteHandler),

    (r'/article/add', article_handler.AddHandler),

    (r'/article/search', article_handler.SearchHandler),






]