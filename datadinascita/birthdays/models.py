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
