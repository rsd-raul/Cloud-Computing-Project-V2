import webapp2


class MainHandler(webapp2.RequestHandler):

    def get(self):  # pylint:disable-msg=invalid-name
        """Handle GET requests."""
        self.response.write("""<h2>Hello, world!!!</h2>""")


APP = webapp2.WSGIApplication([('/.*', MainHandler), ], debug=True)

