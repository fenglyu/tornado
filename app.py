#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.escape
import tornado.gen
import tornado.escape
import logging
import os

import uimodules

logging.basicConfig(
    level=logging.DEBUG,
    format=
    '%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d %(message)s', )


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(
            '<html><body>'
            '<br><a href="/msg">Message</a>'
            '<br><a href="/fetch_async">API @tornado.web.asynchronous</a>'
            '<br><a href="/fetch_coro">API @tornado.gen.coroutine</a>'
            '<br><a href="/temp">Template</a>'
            '<br><a href="/uimodule">uimodule</a>'
            '</body></html>')


class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/msg" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("message"))


class FakeJsonAPI(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        feng = dict(name="Feng LYU", gender="male", age=28, )

        sky = dict(name="Sky Zhang", gender="female", age=26, )
        users = (feng, sky)
        json = tornado.escape.json_encode(users)
        self.write(json)


class WebSpiderHandler_Async(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://192.168.56.111:8888/api", callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(json) + " name" "from our own api")
        self.finish()


class WebSpiderHandler_coroutine(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://192.168.56.111:8888/api")
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(json) + "from fake API")


class TemplateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://192.168.56.111:8888/api")
        json = tornado.escape.json_decode(response.body)
        #userlist = [ "Hello" , "hellO", "aaa" , "bbbb" ]
        self.render("index.html",
                    title="Very first template demo",
                    userlist=json)


class UIModuleHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://192.168.56.111:8888/api")
        user1 = User(name="许其亮", age=24, gender="男")
        user2 = User(name="杨雪", age=23, gender="女")
        profiles = [user1, user2]
        self.render("uimodule.html",
                    title="Yet Another Template",
                    profiles=profiles)


class User(object):
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        print escape.xhtml_escape(self.xsrf_token)
        self.render("login.html", welcome="Demo of tornado login", error = None)


    @tornado.gen.coroutine
    @tornado.web.authenticated
    def post(self):
        user = self.get_argument("user")
        password = tornado.escape.utf8(self.get_argument("password"))
        if user == "feng" and password == "111":
            self.set_secure_cookie("feng", str("feng"))
            self.redirect(self.get_argument("next"))
        else:
            self.render("login.html",
                        welcome="Something is wrong",
                        error="username or password wrong")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/msg", MyFormHandler),
            (r"/fetch_async", WebSpiderHandler_Async),
            (r"/api", FakeJsonAPI),
            (r"/fetch_coro", WebSpiderHandler_coroutine),
            (r"/temp", TemplateHandler),
            (r"/uimodule", UIModuleHandler),
            (r"/login", LoginHandler),
        ]
        settings = dict(autoreload=True,
                         debug=True,
                         compress_response=True,
                         template_path=os.path.join(
                             os.path.dirname(__file__), "templates"),
                         compiled_template_cache=False,
                         cookie_secret="__suning_secret__",
                         login_url="/login",
                         xsrf_cookies=True,
                         ui_modules=uimodules, )
        super(Application, self).__init__(handlers, **settings)


def make_app():
    return Application()


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
