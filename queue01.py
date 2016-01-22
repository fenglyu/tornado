#!/usr/bin/evn python

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue


q = Queue(maxsize=2)


@gen.coroutine
def consumer():
    while True:
        item = yield q.get()
        try:
            print('Doing work on %s' % item)
            yield gen.sleep(0.01)
        finally:
            q.task_done


@gen.coroutine
def producer():
    for i in range(5):
        yield q.put(i)
        print('Put %s' % i)


@gen.coroutine
def main():
    IOLoop.current().spawn_callback(consumer)
    yield producer()
    yield q.join()
    print('Done')

IOLoop.current().run_sync(main)
