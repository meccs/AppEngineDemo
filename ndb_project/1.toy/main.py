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
    created_at = ndb.DateTimeProperty( auto_now_add=True )


class FormHandler(webapp2.RequestHandler):
    def post(self):
        form_title = self.request.get('title')
        new_comment = Comment( title = form_title)
        new_comment.put()
        self.redirect('/')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # display information from database
        q = Comment.query().order(-Comment.created_at).fetch()
        template_values = {'name':'YOUR_USER_NAME', 'q': q}
        template = ENV.get_template('index.html')
        self.response.write(template.render(template_values))
 

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

