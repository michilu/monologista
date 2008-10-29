# vim: fileencoding=utf8

import os
import string
import random
import unittest

from google.appengine.api import (apiproxy_stub_map,
                                  datastore_file_stub,
                                  mail_stub,
                                  urlfetch_stub,
                                  user_service_stub)
from google.appengine.ext import db, search
from google.appengine.api import users

from models import *

APP_ID = u'monologista'
AUTH_DOMAIN = u'gmail.com'
#USER_EMAIL = u'test@example.com'

class TestDatastore(unittest.TestCase):
  """
  """
  def create_account(self, account_id):
    user = users.User(email=(account_id + '@example.com'))
    account = Account(key_name=account_id, user=user, account_id=account_id)
    account.put()
    return account

  def setUp(self):
    os.environ['APPLICATION_ID'] = APP_ID
    os.environ['AUTH_DOMAIN'] = AUTH_DOMAIN
    #os.environ['USER_EMAIL'] = USER_EMAIL
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    stub = datastore_file_stub.DatastoreFileStub(APP_ID, '/dev/null', '/dev/null')
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
    apiproxy_stub_map.apiproxy.RegisterStub('user', user_service_stub.UserServiceStub())

    self.alice = self.create_account(account_id='alice')
    self.bob = self.create_account(account_id='bob')
    self.carol = self.create_account(account_id='carol')
    self.dave = self.create_account(account_id='dave')

  def update_clip(self, clip):
    for follower in clip.account.followers:
      follower.timeline.append(clip.key())
      follower.put()
    else:
      account = clip.account
      account.timeline.append(clip.key())
      account.put()

  def test_clip_append_or_remove(self):
    alice = self.alice
    bob = self.bob
    carol = self.carol

    bob.followings.append(alice.key())
    bob.put()

    carol.followings.append(alice.key())
    carol.put()

    self.failUnlessEqual(len(bob.followings), 1)
    self.failUnlessEqual(len(carol.followings), 1)

    self.failUnlessEqual(alice.followers.count(), 2)

    clip = Clip(account=alice, url='http://www.google.com', title='google')
    clip.put()
    self.update_clip(clip)

    self.failUnlessEqual(len(alice.timeline), 1)
    bob = Account.get_by_key_name('bob')
    self.failUnlessEqual(len(bob.timeline), 1)
    carol = Account.get_by_key_name('carol')
    self.failUnlessEqual(len(carol.timeline), 1)

    self.failUnlessEqual(len(alice.followings), 0)
    self.failUnlessEqual(len(bob.followings), 1)
    self.failUnlessEqual(len(carol.followings), 1)

    self.failUnlessEqual(alice.followers.count(), 2)
    self.failUnlessEqual(bob.followers.count(), 0)
    self.failUnlessEqual(carol.followers.count(), 0)

  def update_status(self, status):
    for follower in status.account.followers:
      follower.timeline.append(status.key())
      follower.put()
    else:
      account = status.account
      account.timeline.append(status.key())
      account.put()

  def test_status_append_or_remove(self):
    alice = self.alice
    bob = self.bob
    carol = self.carol

    bob.followings.append(alice.key())
    bob.put()

    carol.followings.append(alice.key())
    carol.put()

    #alice = Account.get_by_key_name('alice')
    #bob = Account.get_by_key_name('bob')
    #carol = Account.get_by_key_name('carol')

    self.failUnlessEqual(len(alice.followings), 0)
    self.failUnlessEqual(len(bob.followings), 1)
    self.failUnlessEqual(len(carol.followings), 1)

    self.failUnlessEqual(alice.followers.count(), 2)
    self.failUnlessEqual(bob.followers.count(), 0)
    self.failUnlessEqual(carol.followers.count(), 0)

    status = Status(account=alice, status='hello world')
    status.put()
    self.update_status(status)

    alice = Account.get_by_key_name('alice')
    self.failUnlessEqual(len(alice.timeline), 1)
    bob = Account.get_by_key_name('bob')
    self.failUnlessEqual(len(bob.timeline), 1)
    carol = Account.get_by_key_name('carol')
    self.failUnlessEqual(len(carol.timeline), 1)

    alice = Account.get_by_key_name('alice')
    bob = Account.get_by_key_name('bob')
    carol = Account.get_by_key_name('carol')

    self.failUnlessEqual(len(alice.followings), 0)
    self.failUnlessEqual(len(bob.followings), 1)
    self.failUnlessEqual(len(carol.followings), 1)

    self.failUnlessEqual(alice.followers.count(), 2)
    self.failUnlessEqual(bob.followers.count(), 0)
    self.failUnlessEqual(carol.followers.count(), 0)

  def test_following_append_or_remove(self):
    """
    """
    alice = self.alice
    bob = self.bob
    carol = self.carol

    alice.followings.append(bob.key())
    alice.put()
    self.failUnlessEqual(len(alice.followings), 1)
    alice.followings.append(carol.key())
    alice.put()
    self.failUnlessEqual(len(alice.followings), 2)

    alice.followings.remove(bob.key())
    alice.put()
    self.failUnlessEqual(len(alice.followings), 1)
    alice.followings.remove(carol.key())
    alice.put()
    self.failUnlessEqual(len(alice.followings), 0)

    alice = Account.get_by_key_name('alice')
    bob = Account.get_by_key_name('bob')
    carol = Account.get_by_key_name('carol')

    self.failUnlessEqual(len(alice.followings), 0)
    self.failUnlessEqual(len(bob.followings), 0)
    self.failUnlessEqual(len(carol.followings), 0)

    self.failUnlessEqual(alice.followers.count(), 0)
    self.failUnlessEqual(bob.followers.count(), 0)
    self.failUnlessEqual(carol.followers.count(), 0)

  def test_followers_append_or_remove(self):
    alice = self.alice
    bob = self.bob
    carol = self.carol

    bob.followings.append(alice.key())
    bob.put()
    carol.followings.append(alice.key())
    carol.put()

    self.failUnlessEqual(len(bob.followings), 1)
    self.failUnlessEqual(len(carol.followings), 1)

    alice = Account.get_by_key_name('alice')

    self.failUnlessEqual(len(alice.followings), 0)
    self.failUnlessEqual(alice.followers.count(), 2)

    bob.followings.remove(alice.key())
    bob.put()
    carol.followings.remove(alice.key())
    carol.put()

    alice = Account.get_by_key_name('alice')
    bob = Account.get_by_key_name('bob')
    carol = Account.get_by_key_name('carol')

    self.failUnlessEqual(len(alice.followings), 0)
    self.failUnlessEqual(len(bob.followings), 0)
    self.failUnlessEqual(len(carol.followings), 0)

    self.failUnlessEqual(alice.followers.count(), 0)
    self.failUnlessEqual(bob.followers.count(), 0)
    self.failUnlessEqual(carol.followers.count(), 0)

  def test_timeline(self):
    alice = self.alice
    bob = self.bob
    carol = self.carol

    bob.followings.append(alice.key())
    bob.put()

    carol.followings.append(alice.key())
    carol.put()

    alice = Account.get_by_key_name('alice')
    bob = Account.get_by_key_name('bob')
    carol = Account.get_by_key_name('carol')

    self.failUnlessEqual(len(alice.followings), 0)
    self.failUnlessEqual(len(bob.followings), 1)
    self.failUnlessEqual(len(carol.followings), 1)

    self.failUnlessEqual(alice.followers.count(), 2)
    self.failUnlessEqual(bob.followers.count(), 0)
    self.failUnlessEqual(carol.followers.count(), 0)


if __name__ == '__main__':
    unittest.main()

