#!/usr/bin/env python

class Profile(tornado.web.UIModule):
	def render(self, profile):
		return self.render_string("profile.html", profile = profile)
