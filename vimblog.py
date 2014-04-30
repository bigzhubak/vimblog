#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web

HTML_PATH = '/home/bigzhu/Dropbox/knowledge/html/'


def getHtmlContent(name):
    name_file = open(HTML_PATH + name + '.html', 'r')
    content = name_file.read()
    name_file.close()
    return content


class blog(tornado.web.RequestHandler):
    def get(self, name):
        content = getHtmlContent(name)
        print content
        self.render("./template/detail.html", title=name, content=content)


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    '''不要cache static 的文件'''
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


settings = {'debug': True, 'cookie_secret': 'bigzhu so big', 'autoescape': None}
url_map = [
    (r'/blog/(.*)', blog),
    (r'/static/(.*)', MyStaticFileHandler, {'path': "./static"})
]
application = tornado.web.Application(url_map, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
