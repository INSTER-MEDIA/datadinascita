from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from datadinascita.birthdays.models import Person

import logging
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

            for row in stringReader:
            #            Very ugly
            #            TODO: Optimize, remove redundant datastore queries
                people = Person.all().filter("owner =", users.get_current_user())
                if people.filter("name =", row[1].decode('utf-8')).count() == 0:
                    p = Person(name=row[1].decode('utf-8'))
                    p.owner = users.get_current_user()
                    p.birthday = datetime.date(datetime.strptime(row[0], "%m/%d/%Y"))
                    p.put()

            self.redirect('/')
        except:
            self.redirect('upload_failure')


class fail(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
            <html>
            <body>
                <h1 style="color: Red;">Failed</h1>
                <p>Possibly, file is too big or not csv</p>
				<p>Valid csv:</p>
				<p><img src="/images/import.png" alt="Import" border="0" /></p>
                <a href="/import/">Try again</a>
            <body>
            <html>
                                ''')

class test(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <title>Grid with RowEditor Example</title>
    <link rel="stylesheet" type="text/css" href="/js/resources/css/ext-all.css" />
    <link rel="stylesheet" type="text/css" href="/js/examples/grid/grid-examples.css" />
    <!-- Common Styles for the examples -->
    <link rel="stylesheet" type="text/css" href="/js/examples/shared/examples.css" />
    <link rel="stylesheet" type="text/css" href="/js/examples/ux/css/RowEditor.css" />
	<style type="text/css">
		.x-grid3 .x-window-ml{
			padding-left: 0;	
		} 
		.x-grid3 .x-window-mr {
			padding-right: 0;
		} 
		.x-grid3 .x-window-tl {
			padding-left: 0;
		} 
		.x-grid3 .x-window-tr {
			padding-right: 0;
		} 
		.x-grid3 .x-window-tc .x-window-header {
			height: 3px;
			padding:0;
			overflow:hidden;
		} 
		.x-grid3 .x-window-mc {
			border-width: 0;
			background: #cdd9e8;
		} 
		.x-grid3 .x-window-bl {
			padding-left: 0;
		} 
		.x-grid3 .x-window-br {
			padding-right: 0;
		}
		.x-grid3 .x-panel-btns {
			padding:0;
		}
		.x-grid3 .x-panel-btns td.x-toolbar-cell {
			padding:3px 3px 0;
		}
		.x-box-inner {
			zoom:1;
		}
        .icon-user-add {
            background-image: url(/js/examples/shared/icons/fam/user_add.gif) !important;
        }
        .icon-user-delete {
            background-image: url(/js/examples/shared/icons/fam/user_delete.gif) !important;
        }        
    </style>
    
    <!-- GC --><!-- LIBS -->
    <script type="text/javascript" src="/js/adapter/ext/ext-base.js"></script>
    <script type="text/javascript" src="/js/ext-all.js"></script>
    <script type="text/javascript" src="/js/examples/grid/gen-names.js"></script>
    <script type="text/javascript" src="/js/examples/ux/RowEditor.js"></script>
    <script type="text/javascript" src="/js/ddn_list.js"></script>
</head>
<body>
<div id="list_container"></div>
</body>
</html>


                                ''')

application = webapp.WSGIApplication([
                                             ('/upload_csv/', UploadHandler),
                                             ('/test/', test),
                                             ('/upload_failure/', fail),
                                             ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
