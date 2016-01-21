#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.escape
import tornado.gen
import logging

logging.basicConfig(
		level = logging.DEBUG,
		format = '%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d %(message)s',
		)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('<html><body>'
			'<br><a href="/msg">Message</a>'
			'<br><a href="/fetch_async">API @tornado.web.asynchronous</a>'
			'<br><a href="/fetch_coro">API @tornado.gen.coroutine</a>'
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
		feng = dict(
				name = "Feng LYU",
				gender = "male",
				age = 28,
		)

		sky = dict(
				name = "Sky Zhang",
				gender = "female",
				age = 26,
		)
		users = ( feng, sky )
		json = tornado.escape.json_encode(users)
		self.write(json)

class WebSpiderHandler_Async(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		http = tornado.httpclient.AsyncHTTPClient()
		http.fetch("http://192.168.56.111:8888/api", callback=self.on_response)

	def on_response(self, response):
		if response.error: raise tornado.web.HTTPError(500)
		json = tornado.escape.json_decode(response.body)
		self.write("Fetched " + str(json) +" name"
				"from our own api")
		self.finish()

class WebSpiderHandler_coroutine(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def get(self):
		http = tornado.httpclient.AsyncHTTPClient()
		response = yield http.fetch("http://192.168.56.111:8888/api")
		json = tornado.escape.json_decode(response.body)
		self.write("Fetched " + str(json) + "from fake API")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/msg", MyFormHandler),
			(r"/fetch_async", WebSpiderHandler_Async),
			(r"/api", FakeJsonAPI),
			(r"/fetch_coro", WebSpiderHandler_coroutine),
		]
		setttings = dict(
			autoreload	= True,
			debug		= True,
			compress_response = True,
		#	xsrf_cookies = True,
		)
		super(Application, self).__init__(handlers, **setttings)

def make_app():
	return Application()

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
