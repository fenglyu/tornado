#!/usr/bin/env python

# -*- coding: utf-8 -*-

import datetime
import json

import tornado.httpserver
import tornado.web
import tornado.httpclient
from tornado.options import define, options

define("port", default=8000, help="run on given port", type=int)

class Base(tornado.web.RequestHandler):
    pass


class Index(Base):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,
                "http://opsdevpre.cnsuning.com/")
        body = response.body
        now = datetime.datetime.utcnow()
        self.write("""
            <div style="text-align: center">
                       <div style="font-size: 72px">%s</div>
                   </div>.
                   <div>%s</div>
                   """ % (body, now))
        self.finish()


    def post(self, data):
        pass




if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = dict(
        auto_reload = True,
    )

    app = tornado.web.Application([
        (r'/', Index)
    ], **settings)


    http_sever = tornado.httpserver.HTTPServer(app)
    http_sever.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
