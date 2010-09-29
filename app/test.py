import os

from google.appengine.ext.webapp import template

__author__ = 'oleg'

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class test(webapp.RequestHandler):
    def get(self, slash, params):
        template_values = {
            'params': params,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/test.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                [
                (r'/test(/?)(.*)', test),
                ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

