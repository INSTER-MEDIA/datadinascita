from django.conf.urls.defaults import *

urlpatterns = patterns('datadinascita.birthdays.views',
   (r'^$', 'list'),
   (r'^people/$', 'people'),
   (r'^list/$', 'list'),
   (r'^new/$', 'new'),
   (r'^add/$', 'add'),
   (r'^edit/(.*)/$', 'edit'),
   (r'^erase/$', 'erase'),
   (r'^search/$', 'search'),
   (r'^import/$', 'csv_upload'),
   (r'^import_failed/$', 'import_failed'),
   (r'^export/$', 'export'),
)

urlpatterns += patterns(
    'datadinascita.birthdays.tests',
    (r'^djtest/$', 'test'),
)

urlpatterns += patterns(
    'datadinascita.birthdays.views',
    (r'^(.*)$', 'fof'),
)