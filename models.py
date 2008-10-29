# vim: fileencoding=utf8

import string
import random

from google.appengine.ext import db
from google.appengine.api import users

LETTERS_AND_DIGITS = string.letters + string.digits

"""
"""

class Account(db.Model):
  """
  >>> users.User()
  >>> account = Account(key_name='spam')
  """
  user = db.UserProperty(required=True)
  account_id = db.StringProperty(required=True)
  access_key_id = db.StringProperty(default=self.generate_random_string(20))
  secret_access_key = db.StringProperty(default=self.generate_random_string(20))
  timeline = db.ListProperty(db.Key)
  followings = db.ListProperty(db.Key)
  image = db.BlobProperty(required=False)
  created = db.DateTimeProperty(auto_now_add=True)

  @property
  def followers(self):
    """
    >>> for i in account.followers: Account.get_by_key(i)
    """
    return Account.all().filter('followings =', self.key())

  def generate_random_string(self, length):
    return ''.join([random.choice(LETTERS_AND_DIGITS) for i in range(length)])

class Tag(db.Model):
  name = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)

  def statuses(self):
    return Status.all().filter('tags =', self.key())

class Status(db.Model):
  """
  >>> account
  >>> status = Status(parent=account)
  >>> status.account = account
  >>> status.text = 'spam'
  >>> status.put()
  """
  account = db.ReferenceProperty(Account)
  text = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  replies = db.LinkProperty(db.Key)
  tags = db.LinkProperty(db.Key)

