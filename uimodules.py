#!/usr/bin/env python

import tornado


class Profile(tornado.web.UIModule):
    def render(self, profile):
        return self.render_string("user.html", profile=profile)
