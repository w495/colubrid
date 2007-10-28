# -*- coding: utf-8 -*-
from colubrid import PathApplication, Request, HttpResponse
from colubrid.exceptions import PageNotFound


class UploadApplication(PathApplication):
    
    def __init__(self, environ, start_response):
        super(PathApplication, self).__init__(environ, start_response)
        self.request = Request(environ)
    
    def show_index(self, *args):
        return '''
            <html>
            <head><title>Upload Demonstration</title></head>
            <body>
            <h1>Upload Demostration</h1>
            <form action="upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
            </form>
            </body></html>
        '''

    def show_upload(self, *args):
        if args:
            raise PageNotFound
        if 'file' in self.request.files:
            f = self.request.files['file']
            response = HttpResponse(f.data)
            response['Content-Type'] = f.type
            return response

app = UploadApplication


if __name__ == '__main__':
    from colubrid import execute
    execute()
