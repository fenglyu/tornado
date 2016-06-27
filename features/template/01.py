#!/usr/bin/env python

from tornado import template

t = template.Template("<html>{{ demo }}</html>")
print t.generate(demo="aaa")
