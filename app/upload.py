from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from datadinascita.birthdays.models import Person

from google.appengine.ext.blobstore.blobstore import fetch_data
from StringIO import StringIO
import csv
from datetime import datetime


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload_files = self.get_uploads('file')
            blob_info = upload_files[0]
            if blob_info.size > 1048576: # 1Mb
                self.redirect('/upload_failure')

            csv_file = fetch_data(blob_info, 0, blob_info.size + 1)
            stringReader = csv.reader(StringIO(csv_file))
#            TODO: clean up blobstore, or save reference to it

            for row in stringReader:
            #            Very ugly
            #            TODO: Optimize, remove redundant datastore queries
                people = Person.all().filter("owner =", users.get_current_user())
                if people.filter("name =", row[1].decode('utf-8')).count() == 0:
                    p = Person(name=row[1].decode('utf-8'))
                    p.owner = users.get_current_user()
                    p.birthday = datetime.date(datetime.strptime(row[0], "%m/%d/%Y"))
                    p.put()

            self.redirect('/people')
        except:
            self.redirect('/import_failed')


application = webapp.WSGIApplication([
                                             ('/upload_csv/', UploadHandler),
                                             ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
