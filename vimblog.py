#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web
import json
from search_vimwiki import SearchWiki

HTML_PATH = '/home/bigzhu/Dropbox/knowledge/html/'
WIKI_PATH = '/home/bigzhu/Dropbox/knowledge/data/'
key_names = {}
new_key_names = []


def getKeyNames():
    try:
        f = open('./key_name', 'r')
        global key_names
        key_names = json.loads(f.read())
        f.close()
    except IOError:
        pass


def saveKeyNames():
    f = open('./key_name', 'w')
    global key_names
    print >>f, json.dumps(key_names)
    f.close()


def addKeyNamesCount(name):
    global key_names
    if name in key_names:
        key_names[name] += 1
        if key_names[name] % 5 == 0:
            saveKeyNames()
    else:
        key_names[name] = 1


def getList(name):
    seartch_wiki = SearchWiki(name)
    seartch_wiki.search(WIKI_PATH, HTML_PATH)
    seartch_wiki.mergerByYear()
    seartch_wiki.sortByTime()
    seartch_wiki.sortByYear()
    global new_key_names
    if seartch_wiki.mergered_all_sorted:
        new_key_names = seartch_wiki.mergered_all_sorted[0][1][:10]
    return seartch_wiki.mergered_all_sorted


def getHtmlContent(name):
    try:
        name_file = open(HTML_PATH + name + '.html', 'r')
        content = name_file.read()
        name_file.close()
        return content
    except IOError:
        return '0'


class list(tornado.web.RequestHandler):
    def get(self, name='*'):
        lists = getList(str(name))
        if name == '*':
            title = 'bigzhu的窝'
        else:
            title = name
            addKeyNamesCount(name)
        global key_names
        self.render("./template/list.html", title=title, lists=lists, key_names=key_names)


class blog(tornado.web.RequestHandler):
    def get(self, name):
        if name is None:
            name = 'index'
        content = getHtmlContent(name)

        global key_names
        global new_key_names
        self.render("./template/detail.html", title=name, content=content, key_names=key_names, new_key_names=new_key_names)


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    '''不要cache static 的文件'''
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


settings = {'debug': True, 'cookie_secret': 'bigzhu so big', 'autoescape': None, "static_path": os.path.join(os.path.dirname(__file__), "static"), }
url_map = [
    (r'/', list),
    (r'/blog/(.*)', blog),
    (r'/list/(.*)', list),
]
application = tornado.web.Application(url_map, **settings)

if __name__ == "__main__":
    getKeyNames()
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    #print getList('search_vimwiki')
