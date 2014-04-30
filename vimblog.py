#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import public

OK = '0'


class blog(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world, haha")


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    '''不要cache static 的文件'''
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


the_globals = globals().copy()
url_map = public.getURLMap(the_globals)

settings = {'debug': True,
            'cookie_secret': 'bigzhu so big',
            'login_url': "/static/login.html"}
url_map.append((r'/static/(.*)', MyStaticFileHandler, {'path': "./static"}))

application = tornado.web.Application(url_map, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
