#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging
import os.path
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

DEBUG = False 

def send_message(message):
    for handler in ChatSocketHandler.socket_handlers:
        try:
            handler.write_message(message)
        except:
            logging.error('Error sending message', exc_info=True)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    socket_handlers = set()

    def open(self):
        ChatSocketHandler.socket_handlers.add(self)
        logging.error('login')

    def on_close(self):
        ChatSocketHandler.socket_handlers.remove(self)

    def on_message(self, message):
        send_message(message)


def main(port):
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'debug': DEBUG
    }
    application = tornado.web.Application([
        ('/', MainHandler),
        ('/new-msg/socket', ChatSocketHandler),
        (r"/(crossdomain\.xml)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main(int(sys.argv[1]))
