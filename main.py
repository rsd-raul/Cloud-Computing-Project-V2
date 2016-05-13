from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
from time import sleep


# Declaration of our model, in this case: title, format, date and file(its key)
class FileModel(ndb.Model):
    title = ndb.StringProperty()
    format = ndb.StringProperty()
    # This will automatically add the date of creation without forcing us to do it manually
    date = ndb.DateTimeProperty(auto_now_add=True)
    blob_key = ndb.BlobKeyProperty()


class FileUploadFormHandler(webapp2.RequestHandler):
    def get(self):
        files = FileModel.query()

        self.response.write('''
            <html>
                <meta charset="UTF-8">
                <head>
                    <title>Objects in the DataStore</title>
                    <link rel="stylesheet" type="text/css" href="styles\style.css">
                    <style type="text/css">
                    h2 { color: blue; }
                    </style>
                </head>
                <body>
                    <main>
                        <h1>Objects in the DataStore</h1>
                            ''')

        exists = False
        for aux_file in files:
            if not exists:
                self.response.write('''
                        <h2>Select one to download</h2>
                        <form action="download_file/">
                                    ''')
                exists = True

            self.response.write('''
                            <input type="checkbox" name="id" value={0}> {1} -- {2}<br>
                                '''.format(aux_file.blob_key, aux_file.title, aux_file.date))

        if exists:
            self.response.write('''
                            <br>
                            <input type="submit" value="Download">
                        </form>
                                ''')

        upload_url = blobstore.create_upload_url('/upload_file')

        self.response.out.write('''
                        <h2>Upload a file:</h2>

                        <!-- The form must be enctype="multipart/form-data" for Blobstore.-->
                        <form action="{0}" method="POST" enctype="multipart/form-data">
                            Upload File: <input type="file" name="file">
                            <br><br>
                            <input type="submit" name="submit" value="Submit">
                        </form>
                    </main>
                </body>
            </html>
                                '''.format(upload_url))


class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            # We get from all the upload files the first one, in this case, there wont be more than 1 file
            upload = self.get_uploads()[0]

            # We create an instance of FileModel by initializing all the properties with the info of the file uploaded
            new_file = FileModel(
                title=upload.filename,
                format=upload.content_type,
                blob_key=upload.key())
            # Then we commit that transaction to the DataStore
            new_file.put()

            # Added 1 second before redirect so changes are stored and shown
            sleep(1)
            self.redirect('/')

        except:
            self.error(500)


class DownloadFile(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, file_key):

        # Retrieve the file key by asking for the id parameter we set in the form
        file_key = self.request.get("id")

        # If there is no such file, redirect to a 404 page
        if not blobstore.get(file_key):
            self.error(404)
        # If there is, send it to download
        else:
            self.send_blob(file_key)


APP = webapp2.WSGIApplication([
    ('/', FileUploadFormHandler),
    ('/upload_file', FileUploadHandler),
    ('/download_file/(.*)', DownloadFile),
], debug=True)
