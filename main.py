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

        self.response.write('<h1>Object in the Datastore</h1>'
                            '<ol>')

        self.response.write('''
        <h2>Select one to download</h2>
        <form action="download_file/">
        ''')
        for aux_file in files:
            self.response.write('''
                <input type="checkbox" name="id" value={0}> {1} - {2}<br>
            '''.format(aux_file.blob_key, aux_file.title, aux_file.date))

        self.response.write('''<br><input type="submit" value="Submit"></form>''')

        upload_url = blobstore.create_upload_url('/upload_file')

        self.response.out.write("""<h2>Upload a file instead:</h2>""")
        self.response.out.write("""
            <html><body>
            <form action="{0}" method="POST" enctype="multipart/form-data">
              Upload File: <input type="file" name="file">
              <br><br>
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
            self.error(500)


class DownloadFile(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, file_key):

        # Retrieve the file key by asking for the id parameter we set in the form
        file_key = self.request.get("id")

        if not blobstore.get(file_key):
            self.error(404)
        else:
            self.send_blob(file_key)


APP = webapp2.WSGIApplication([
    ('/', FileUploadFormHandler),
    ('/upload_file', FileUploadHandler),
    ('/download_file/(.*)', DownloadFile),
], debug=True)