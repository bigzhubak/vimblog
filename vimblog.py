#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from search_vimwiki import SearchWiki

HTML_PATH = '/home/bigzhu/Dropbox/knowledge/html/'
WIKI_PATH = '/home/bigzhu/Dropbox/knowledge/data/'


def getList(name):
    seartch_wiki = SearchWiki(name)
    seartch_wiki.search(WIKI_PATH)
    seartch_wiki.search()
    seartch_wiki.mergerByYear()
    seartch_wiki.sortByTime()
    seartch_wiki.sortByYear()
    return seartch_wiki.mergered_all_sorted


def getHtmlContent(name):
    name_file = open(HTML_PATH + name + '.html', 'r')
    content = name_file.read()
    name_file.close()
    return content


class list(tornado.web.RequestHandler):
    def get(self, name='*'):
        lists = getList(name)
        self.render("./template/list.html", title=name, lists=lists)


class blog(tornado.web.RequestHandler):
    def get(self, name):
        if name is None:
            name = 'index'
        content = getHtmlContent(name)
        self.render("./template/detail.html", title=name, content=content)


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    '''不要cache static 的文件'''
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


settings = {'debug': True, 'cookie_secret': 'bigzhu so big', 'autoescape': None}
url_map = [
    (r'/', list),
    (r'/blog/(.*)', blog),
    (r'/list/(.*)', list),
    (r'/static/(.*)', MyStaticFileHandler, {'path': "./static"})
]
application = tornado.web.Application(url_map, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    #getList('bigzhu')
