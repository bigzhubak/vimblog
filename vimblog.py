#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web
import json
from search_vimwiki import SearchWiki

HTML_PATH = '/home/bigzhu/Dropbox/knowledge/html/'
WIKI_PATH = '/home/bigzhu/Dropbox/knowledge/data/'
SITE = 'site'
key_names = {}
key_names_sorted = []
new_key_names = []


def getKeyNames():
    try:
        f = open('./key_name', 'r')
        global key_names
        global key_names_sorted
        key_names = json.loads(f.read())
        key_names_sorted = sorted(key_names.items(), key=lambda by: by[1], reverse=True)
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
        if name.strip() != "":
            key_names[name] = 1
        #需要排序
    global key_names_sorted
    key_names_sorted = sorted(key_names.items(), key=lambda by: by[1], reverse=True)


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
        global key_names_sorted
        self.render("./template/list.html", title=title, lists=lists, key_names=key_names_sorted)


class blog(tornado.web.RequestHandler):
    def get(self, name):
        if name is None:
            name = 'index'
        html = name.rsplit('.', 1)
        if len(html) > 1 and html[1] == 'html':
            name = html[0]
        content = getHtmlContent(name)
        site = getHtmlContent(SITE)

        global key_names
        global key_names_sorted
        global new_key_names
        self.render("./template/detail.html", title=name, content=content, key_names=key_names_sorted, new_key_names=new_key_names, site=site)


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
    (r'/(.*)', blog),
]
application = tornado.web.Application(url_map, **settings)

if __name__ == "__main__":
    getKeyNames()
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
    #print getList('search_vimwiki')
