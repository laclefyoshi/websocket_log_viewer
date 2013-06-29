#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

import tornado.ioloop
import tornado.websocket
import sys
import cgi
import Queue
from threading import Thread
import time

ioloop = tornado.ioloop.IOLoop.instance()

def connected(result):
     client = result.result()
     for line in iter(sys.stdin.readline, ""):
          client.write_message(cgi.escape(line.rstrip()))
     ioloop.stop()

def main(url):
    status = tornado.websocket.websocket_connect(url, io_loop=ioloop, callback=connected)
    ioloop.start()

if __name__ == "__main__":
    main("ws://localhost:8899/ws")


