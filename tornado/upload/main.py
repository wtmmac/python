#!/usr/bin/env python
# coding=utf-8
import tornado.ioloop  
import tornado.web  
import os, datetime, time

APP_ROOT = os.path.dirname(__file__)

  
class MainHandler(tornado.web.RequestHandler):  
    def get(self):  
        self.render(os.path.join(APP_ROOT, 'index.html'))  
  
class UploadHandler(tornado.web.RequestHandler):  
    def post(self):  
        if self.request.files:  
            uploadFile = self.request.files['myfile'][0]
            fileName =  time.strftime("%Y%m%d%H%M%S") + '%d' % datetime.datetime.now().microsecond + '.' + uploadFile["filename"].split('.', 1)[1] 
            fin = open(os.path.join(APP_ROOT, "upload", fileName),"w")    
            fin.write(uploadFile["body"])  
            fin.close()
            self.write("uploaded!")
            print(uploadFile)

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": False,
    "debug": True,
}

application=tornado.web.Application([
    (r'/',MainHandler),
    #(),
    (r'/upload', UploadHandler) 
], **settings)  
  
if __name__=='__main__':  
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()
