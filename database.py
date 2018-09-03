from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    listOfWords = ndb.StringProperty(repeated=True)
