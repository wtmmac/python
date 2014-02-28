#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

DEBUG = True

def send_message(message, uid=None):
    for handler in ChatSocketHandler.socket_handlers:
        try:
            #if uid is not None and handler.uid == uid :
            handler.write_message(message)
            #else:
            #   pass
            #if DEBUG:
            #    print handler.uid
        except:
            logging.error('Error sending message', exc_info=True)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class ReceiveHandler(tornado.web.RequestHandler):
    """
    接收外部消息
    """
    def get(self):
        send_message("to1212121211212121212211221212")

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    socket_handlers = set()

    uid = None

    def open(self):
        ChatSocketHandler.socket_handlers.add(self)
        send_message('A new user has entered the chat room.', None)

    def on_close(self):
        ChatSocketHandler.socket_handlers.remove(self)
        send_message('A user has left the chat room.', None)

    def on_message(self, message):
        if "u:" in message:
            self.uid = message
        send_message(message, None)


def main():
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'debug': DEBUG
    }
    application = tornado.web.Application([
        ('/', MainHandler),
        ('/new-msg/', ChatSocketHandler),
        ('/new-msg/socket', ChatSocketHandler),
        ('/rev', ReceiveHandler)
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()