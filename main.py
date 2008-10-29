# vim: fileencoding=utf8

import os
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

from models import *

"""
"""

class MainHandler(webapp.RequestHandler):
  def get(self):
    return self.response.out.write('Hello world!')

class PublicTimelineHandler(webapp.RequestHandler):
  def get(self):
    public_timeline = Status.all()

    template_values = {
      'public_timeline': public_timeline,
    }

    path = os.path.join(os.path.dirname(__file__), 'public_timeline.html')
    self.response.out.write(template.render(path, template_values))

class HomeTimelineHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    account = Account.all().filter('user =', user).get()
    if not user or not account:
      return self.redirect("/")

    home_timeline = account.timeline.all()

    template_values = {
      'home_timeline': home_timeline,
      'account': account,
    }

    path = os.path.join(os.path.dirname(__file__), 'home_timeline.html')
    self.response.out.write(template.render(path, template_values))

class UserTimelineHandler(webapp.RequestHandler):
  def get(self):
    user_timeline = Status.all().filter('account =', account)

    template_values = {
      'user_timeline': user_timeline,
    }

    path = os.path.join(os.path.dirname(__file__), 'user_timeline.html')
    self.response.out.write(template.render(path, template_values))

class FollowingHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    account = Account.all().filter('user =', user).get()
    if not user or not account:
      return self.redirect("/")

    template_values = {
      'followings': account.followings,
      'account': account,
    }

    path = os.path.join(os.path.dirname(__file__), 'followings.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    pass

class FollowersHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    account = Account.all().filter('user =', user).get()
    if not user or not account:
      return self.redirect("/")

    template_values = {
      'followers': account.followers,
      'account': account,
    }

    path = os.path.join(os.path.dirname(__file__), 'followers.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    pass

def main():
  application = webapp.WSGIApplication([(r'/', MainHandler),
                                        (r'/home/', MainHandler),
                                        (r'/(.*)/', MainHandler),
                                        (r'/(.*)/(.*)', MainHandler),
                                        (r'/(.*)/following/', FollowingHandler),
                                        (r'/(.*)/followers/', FollowersHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
