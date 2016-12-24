#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./lib_p_bz')
import tornado.ioloop
import tornado.web
import json
import time
from search_vimwiki import SearchWiki

from os.path import expanduser
import tornado_bz
import sys
import public_bz
from tornado_bz import BaseHandler
import oper

home = expanduser("~")

HTML_PATH = home + '/Dropbox/knowledge/html/'
WIKI_PATH = home + '/Dropbox/knowledge/data/'
CLICK_COUNT = home + '/click_count'
click_path = home + '/click/'

SITE = 'site'
key_names = {}
key_names_sorted = []
new_key_names = []
click_count = {}
black_keys = ['11', u'香港']

import ConfigParser
config = ConfigParser.ConfigParser()
with open('conf.ini', 'r') as cfg_file:
    config.readfp(cfg_file)
    TITLE = config.get('data', 'title')
    HTML_PATH = config.get('data', 'html_path')


def popSome():
    global key_names
    for black_key in black_keys:
        if black_key in key_names:
            key_names.pop(black_key)


def getKeyNames():
    try:
        f = open('./key_name', 'a+')
        global key_names
        global key_names_sorted
        content = f.read()
        if content != '':
            key_names = json.loads(content)
            popSome()
            key_names_sorted = sorted(
                key_names.items(),
                key=lambda by: by[1],
                reverse=True)
        f.close()
    except IOError:
        print public_bz.getExpInfoAll()


def getClickCount():
    try:
        f = open(CLICK_COUNT, 'a+')
        global click_count
        content = f.read()
        if content != '':
            click_count = json.loads(content)
        f.close()
    except IOError:
        print public_bz.getExpInfoAll()


def save(file_name, content):
    f = open(file_name, 'w+')
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
    # if key_names[name] % 5 == 0:
    if count != 0:
        key_names[name] = count
        saveKeyNames()
    # 需要排序
    global key_names_sorted
    key_names_sorted = sorted(
        key_names.items(),
        key=lambda by: by[1],
        reverse=True)


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
    if name not in black_keys:
        if seartch_wiki.mergered_all_sorted:
            # new_key_names = seartch_wiki.mergered_all_sorted[0][1][:SHOW_COUNT]
            new_key_names = seartch_wiki.mergered_all_sorted[0][1]
    return seartch_wiki.mergered_all_sorted


def getHtmlContent(name):
    '''
    取得对应名字的 html 文件的内容
    '''
    try:
        name_file = open(HTML_PATH + name + '.html', 'r')
        content = name_file.read()
        name_file.close()
        return content
    except IOError:
        print public_bz.getExpInfoAll()
        return '0'


def getLen(lists):
    count = 0
    for l in lists:
        count += len(l[1])
    return count


class list(BaseHandler):

    '''
    显示 blog 列表
    '''

    def get(self, name='*'):
        html_list = oper.getHtmlListByNameLike(name)
        for html in html_list:
            # html.content = oper.getHtmlContent(html.name)
            html.content = ''
        self.render(tornado_bz.getTName(self, 'index'), title=TITLE, main_list=html_list, time=time)


def getContent(name, count=15, lenght=None):
    ten_names = getList(name)[0][1][:count]
    lists = []
    for i in ten_names:
        c = public_bz.storage()
        c.name = i[0]
        c.time = i[1]
        c.content = getHtmlContent(c.name)
        if lenght:
            print len(c.content)
            if len(c.content) < lenght:
                print 'continue ' + c.name
                continue
        lists.append(c)
    return lists


class main(BaseHandler):

    '''
    blog 首页
    '''

    def get(self, name='*'):
        main_list = oper.getMainList()

        self.render(tornado_bz.getTName(self, 'index'), title=TITLE, main_list=main_list, time=time)


class about(BaseHandler):

    '''
    '''

    def get(self):
        self.render(tornado_bz.getTName(self, 'bigzhu'))


class blog(BaseHandler):

    '''
    显示 blog 的详细内容
    '''

    def get(self, name):
        html = oper.getHtmlByName(name)
        main_list = [html]

        self.render(tornado_bz.getTName(self, 'index'), title=name, main_list=main_list, time=time)


# class rss(BaseHandler):
#
#    '''
#    显示 rss
#    '''
#
#    def get(self, name='*'):
#        title = 'bigzhu的窝'
#        lists = getTenContent(name)
#
#        t = jinja2_bz.getTemplate(self.__class__.__name__, 'xml')
#        html = t.render(title=title, lists=lists, time=time)
#        self.write(html)


class roottxt(BaseHandler):

    '''
    阿里妈妈验证
    '''

    def get(self):
        self.write('756973118a848cc29e3952eee7f79daa')
'''
url_map = [
    (r'/root.txt', roottxt),
    (r'/', main),
    (r'/list', list),
    (r'/rss', rss),
    (r'/blog/(.*)', blog),
    (r'/list/(.*)', list),
    (r'/(.*)', blog),
]

settings = tornado_bz.getSettings()
settings['debug'] = False
application = tornado.web.Application(url_map, **settings)
'''

if __name__ == "__main__":
    pg = None
    the_class = globals().copy()

    getKeyNames()
    # getClickCount()

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8888
    print port

    url_map = tornado_bz.getURLMap(the_class)
    url_map.append((r'/', main))
    url_map.append((r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static"}))

    settings = tornado_bz.getSettings()

    settings["pg"] = pg

    application = tornado.web.Application(url_map, **settings)

    application.listen(port)
    ioloop = tornado.ioloop.IOLoop().instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
