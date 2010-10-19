from google.appengine.ext import db

# Create your models here.
class Person(db.Model):
    name = db.StringProperty(required=True)
    birthday = db.DateProperty()
    owner = db.UserProperty()

class Event(db.Model):
    type = db.StringProperty()
    name = db.StringProperty()
    date = db.DateProperty()

class Contact(db.Model):
    name = db.StringProperty(required=True)
    owner = db.UserProperty(required=True)
    event = db.ReferenceProperty(Event)


'''

from google.appengine.api import users
from google.appengine.ext import db
from datadinascita.birthdays.models import Event
from datadinascita.birthdays.models import Contact
from datetime import datetime


# Say hello to the current user
user = users.get_current_user()
if user:
  nickname = user.nickname()
else:
  nickname = "guest"
print "Hello, " + nickname

e = Event(type="birthday",name="Birthday",date=datetime.date(datetime.today()))
e.put()

c = Contact(name="Me",owner=user,event=e)

c1 = Contact(name="Not Me",owner=user,event=e)
c.put()
c1.put()


'''