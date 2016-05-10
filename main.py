from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2


# This datastore model keeps track of which users uploaded which photos.
class FileModel(ndb.Model):
    title = ndb.StringProperty()
    format = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    blob_key = ndb.BlobKeyProperty()


class FileUploadFormHandler(webapp2.RequestHandler):
    def get(self):
        files = FileModel.query()

        self.response.write('<h1>My GuestBook</h1><ol>')
        for aux_file in files:
            self.response.write('<li> \t %s' % aux_file.title)
            self.response.write('''
                <form action="/download_file/{0}" method=get>
                <input type=submit value="Download">
                </form>
            '''.format(aux_file.blob_key))
        self.response.write('</ol>')

        upload_url = blobstore.create_upload_url('/upload_file')

        self.response.out.write("""
            <html><body>
            <form action="{0}" method="POST" enctype="multipart/form-data">
              Upload File: <input type="file" name="file"><br>
              <input type="submit" name="submit" value="Submit">
            </form>
            </body></html>
        """.format(upload_url))


class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            new_file = FileModel(
                title=upload.filename,
                format=upload.content_type,
                blob_key=upload.key())
            new_file.put()

            self.redirect('/')

        except:
            print "este"
            self.error(500)


class DownloadFile(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):

        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)


APP = webapp2.WSGIApplication([
    ('/', FileUploadFormHandler),
    ('/upload_file', FileUploadHandler),
    ('/download_file/(.*)', DownloadFile),
], debug=True)

#
# import webapp2
# from google.appengine.ext import db
# from google.appengine.ext import blobstore
#
#
# class Greeting(db.Model):
#     content = db.StringProperty(multiline=True)
#     date = db.DateTimeProperty(auto_now_add=True)
#
#
# class MainHandler(webapp2.RequestHandler):
#
#     def get(self):  # pylint:disable-msg=invalid-name
#         self.response.write('Hello world!')
#         self.response.write('<h1>My GuestBook</h1><ol>')
#
#         # greetings = db.GqlQuery("SELECT * FROM Greeting")
#         greetings = Greeting.all()
#
#         for greeting in greetings:
#             self.response.write('<li> %s' % greeting.content)
#         self.response.write('''
#             </ol><hr>
#             <form action="/sign" method=post>
#             <textarea name=content rows=3 cols=60></textarea>
#             <br><input type=submit value="Sign Guestbook">
#             </form>
#         ''')
#
#         upload_url = blobstore.create_upload_url('/upload_photo')
#         self.response.out.write("""
#         <html><body>
#         <form action="{0}" method="POST" enctype="multipart/form-data">
#           Upload File: <input type="file" name="file"><br>
#           <input type="submit" name="submit" value="Submit">
#         </form>
#         </body></html>""".format(upload_url))
#
#
# class GuestBook(webapp2.RequestHandler):
#     def post(self):
#         greeting = Greeting()
#         greeting.content = self.request.get('content')
#         greeting.put()
#         self.redirect('/')
#
# APP = webapp2.WSGIApplication([
#     ('/', MainHandler),
#     ('/sign', GuestBook),
# ], debug=True)

