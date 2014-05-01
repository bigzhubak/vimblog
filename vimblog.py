#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web
from search_vimwiki import SearchWiki

HTML_PATH = '/home/bigzhu/Dropbox/knowledge/html/'
WIKI_PATH = '/home/bigzhu/Dropbox/knowledge/data/'
key_names = ['vim', 'python', 'bigzhu']

def getList(name):
    seartch_wiki = SearchWiki(name)
    seartch_wiki.search(WIKI_PATH, HTML_PATH)
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
        lists = getList(str(name))
        if name == '*':
            title = 'bigzhu的窝'
        else:
            title = name
        self.render("./template/list.html", title=title, lists=lists, key_names=key_names)


class blog(tornado.web.RequestHandler):
    def get(self, name):
        if name is None:
            name = 'index'
        content = getHtmlContent(name)
        self.render("./template/detail.html", title=name, content=content, key_names=key_names)


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    '''不要cache static 的文件'''
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


settings = {'debug': True, 'cookie_secret': 'bigzhu so big', 'autoescape': None,
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
            }
url_map = [
    (r'/', list),
    (r'/blog/(.*)', blog),
    (r'/list/(.*)', list),
]
application = tornado.web.Application(url_map, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    #print getList('search_vimwiki')
