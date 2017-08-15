#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import logging
import os
import urllib

import jinja2
import webapp2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        response = urllib.urlopen('https://uinames.com/api/')
        data = response.read()
        template_vars = json.loads(data)
        template = jinja_environment.get_template('template.html')
        self.response.write(template.render(template_vars))

class GifHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('q')
        logging.info("QUERY:" + query)
        base_url = "http://api.giphy.com/v1/gifs/search?"
        url_params = {'q': query, 'api_key': 'dc6zaTOxFJmzC', 'limit': 10}
        giphy_response = urllib.urlopen(base_url + urllib.urlencode(url_params)).read()
        parsed_giphy_dictionary = json.loads(giphy_response)
        gif_url = parsed_giphy_dictionary['data'][0]['images']['original']['url']
        template = jinja_environment.get_template('template.html')
        self.response.write(template.render({'img_url': gif_url}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/gif', GifHandler),
], debug=True)
