#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import tornado.httpserver
import tornado.web
import tornado.httpclient
from uuid import uuid4
from tornado.options import define, options

define("port", default=8000, help="run on given port", type=int)

REMOTE_URL = "http://www.5eplay.com/"


class ShoppingCart(object):
    totalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def moveItemToCart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notifyCallbacks()


    def removeFromCart(self, session):
        if session not in self.carts:
            return

        del(self.carts[session])
        self.notifyCallbacks()



    def notifyCallbacks(self):
        for c in self.callbacks:
            self.callbackHelper(c)

        self.callbacks = []

    def callbackHelper(self, callback):
        callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)


class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.shoppingCart.getInventoryCount()
        self.render("index.html", session=session, count=count)

class CartHandler(tornado.web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')

        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.shoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.shoppingCart.removeItemToCart(session)
        else:
            self.set_status(400)


class StatusHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.application.shoppingCart.register(self.async_callback(self.on_message))

    def on_message(self, count):
        self.write('{"inventoryCount":"%d"}' % count)
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        self.shoppingCart = ShoppingCart()

        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler),
        ]

        settings = {
            'debug': True,
            'template_path': 'templates',
            'static_path': 'statics'
        }

        tornado.web.Application.__init__(self, handlers, **settings)

class Index(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,
                REMOTE_URL)
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

#    app = tornado.web.Application([
#        (r'/', Index)
#    ], **settings)
#

    app = Application()

    http_sever = tornado.httpserver.HTTPServer(app)
    http_sever.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
