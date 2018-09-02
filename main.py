import webapp2
import logging
import jinja2
import os

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('static/main_page.html')
        self.response.write(template.render())

    def post(self):
        logging.info("POST METHOD")

        type = self.request.get('type')
        if type is "login":
            uname = self.request.get('uname')
            psw = self.request.get('psw')
            remember = self.request.get('remember')

            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write("LOGIN QUERY: %s, %s, %s" % (uname, psw, remember))
        elif type is "signup":
            email = self.request.get('email')
            psw = self.request.get('psw')
            psw_repeat = self.request.get('psw-repeat')
            remember = self.request.get('remember')

            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write("LOGIN QUERY: %s, %s, %s, %s" % (email, psw, psw_repeat, remember))

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
], debug=True)
