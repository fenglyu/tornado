#!/usr/bin/env python

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('<html><body>'
				'<a href="/msg">Message</a>'
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


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/msg", MyFormHandler),
		]
		setttings = dict(
			autoreload	= True,
			debug		= True,
			compress_response = True,
			xsrf_cookies = True,
		)
		super(Applicaton, self).__init__(handlers, **setttings)

def make_app():
	return Application

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
