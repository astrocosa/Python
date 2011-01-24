# -*- coding: utf-8 -*-

### Imports ###

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from django.template import TemplateDoesNotExist

### Functions ###

def render(self, file, values={}):
	file = '%s.html' % file
	path = os.path.join(os.path.dirname(__file__), 'views', file)
	if 'title' not in values:
		values['title'] = TITLE
	if 'base' not in values:
		values['base'] = BASE
	try:
		self.response.out.write(template.render(path, values))
	except TemplateDoesNotExist:
		self.error(500)
		self.response.out.write('<b>Error loading template:</b> %s' % path)

def error404(self):
	self.error(404)
	template_values = {
		'subtitle': 'Error 404',
	}
	render(self, 'error404', template_values)

### Handlers ###

class indexHandler(webapp.RequestHandler):
	def get(self):
		render(self, 'index')

class error404Handler(webapp.RequestHandler):
	def get(self):
		error404(self)

### Main code ###

TITLE = 'GAE template'

BASE = 'http://%s' % os.environ['HTTP_HOST']
BASE += '' if BASE[-1] == '/' else '/'

application = webapp.WSGIApplication([
	('/', indexHandler),
	('.*', error404Handler),
], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()
