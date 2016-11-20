#!/usr/bin/env python


class A():
    def __init__(self, *args, **kwargs):
        print("init A")


class B(A):
    def __init__(self, *args, **kwargs):
        print("init B")

u = B()
print(u)
