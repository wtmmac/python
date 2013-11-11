#/usr/bin/env python
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
        # Permission check
  
        if self.request.files:  
            uploadFile = self.request.files['upload_image'][0]
            fileName =  time.strftime("%Y%m%d%H%M%S") + '%d' % datetime.datetime.now().microsecond + '.' + uploadFile["filename"].split('.')[-1].lower()
            uploadPath = time.strftime("%Y/%m/%d")
            uploadRealPath = os.path.join(APP_ROOT, "upload", uploadPath)
            try:
                os.makedirs(uploadRealPath)
            except Exception:
                pass
            uploadRealFilePath = os.path.join(uploadRealPath, fileName)
            uploadedFile = open(uploadRealFilePath, "w")
            uploadedFile.write(uploadFile["body"])
            uploadedFile.close()
            self.write('{"status":200, "file":"%s"}' % os.path.join(uploadPath, fileName))

settings = {
    "debug": True,
}

application = tornado.web.Application([
    (r'/',MainHandler),
    (r'/upload', UploadHandler)
], **settings)

if __name__ == '__main__':
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()
