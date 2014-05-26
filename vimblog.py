#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web
import json
from search_vimwiki import SearchWiki

HTML_PATH = '/home/bigzhu/Dropbox/knowledge/html/'
WIKI_PATH = '/home/bigzhu/Dropbox/knowledge/data/'
CLICK_COUNT = '/home/bigzhu/click_count'
click_path = './click/'

SITE = 'site'
key_names = {}
key_names_sorted = []
new_key_names = []
click_count = {}


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


def getClickCount():
    try:
        f = open(CLICK_COUNT, 'r')
        global click_count
        click_count = json.loads(f.read())
        print click_count
        f.close()
    except IOError:
        print 'IOError'
        pass


def save(file_name, content):
    f = open(file_name, 'w')
    print >>f, json.dumps(content)
    f.close()


def saveKeyNames():
    global key_names
    save('key_name', key_names)


def saveClickCount():
    global click_count
    save(CLICK_COUNT, click_count)


def increase(dic, name):
    if name in dic:
        dic[name] += 1
    else:
        if name.strip() != "":
            dic[name] = 1
    return dic


def refreshKeyNamesCount(name, count):
    global key_names
    #if key_names[name] % 5 == 0:
    if count != 0:
        key_names[name] = count
        saveKeyNames()
    #需要排序
    global key_names_sorted
    key_names_sorted = sorted(key_names.items(), key=lambda by: by[1], reverse=True)


def addClickCount(name):
    global click_count
    click_count = increase(click_count, name)
    save(click_path + name, click_count[name])
    if click_count[name] % 5 == 0:
        saveClickCount()
    return click_count[name]


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


def getLen(lists):
    count = 0
    for l in lists:
        count += len(l[1])
    return count


class list(tornado.web.RequestHandler):
    def get(self, name='*'):
        lists = getList(str(name))
        if name == '*':
            title = 'bigzhu的窝'
        else:
            title = name
            refreshKeyNamesCount(name, getLen(lists))
        global key_names
        global key_names_sorted
        global click_count
        self.render("./template/list.html", title=title, lists=lists, key_names=key_names_sorted, click_count=click_count)


class blog(tornado.web.RequestHandler):
    def get(self, name):
        if name is None:
            name = 'index'
        html = name.rsplit('.', 1)
        if len(html) > 1 and html[1] == 'html':
            name = html[0]
        content = getHtmlContent(name)
        site = None
        site = getHtmlContent(SITE)

        global key_names
        global key_names_sorted
        global new_key_names
        count = addClickCount(name)
        self.render("./template/detail.html", title=name, content=content, key_names=key_names_sorted, new_key_names=new_key_names, site=site, count=count)


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
    getClickCount()
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
