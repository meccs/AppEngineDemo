'''
ndb sample program

'''
import webapp2
import jinja2 
from google.appengine.ext import ndb
import logging

ENV = jinja2.Environment( loader= jinja2.FileSystemLoader("templates"))

# define this model
class Comment(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    created_at = ndb.DateTimeProperty( auto_now_add=True )


class FormHandler(webapp2.RequestHandler):
    def get(self):
        # https://en.wikipedia.org/wiki/Meta_refresh
        self.response.headers['Refresh'] = '0;url="/"'

    def post(self):
        form_title = self.request.get('title')
        form_content = self.request.get('content')

        new_comment = Comment( title = form_title, content = form_content)
        new_comment.put()

        # self.redirect('/')  # old
        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        self.redirect('/processform')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # display information from database
        comments = Comment.query().order(-Comment.created_at).fetch()
        template_values = {'name':'YOUR_USER_NAME', 'comments': comments}
        template = ENV.get_template('index.html')
        self.response.write(template.render(template_values))
 
    def post(self):
        # we don't handle post requests from MainHandler
        self.response.write(" it's not for you Jen ")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/processform', FormHandler),
], debug=True)


'''
Note:
	you can also test ndb from admin console
	Navigate to: http://localhost:8000/console
	from main import Comment
	q = Comment.query().fetch()
	print q
'''

