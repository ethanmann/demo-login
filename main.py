import webapp2
import logging
import jinja2
import os
import database

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def plainTextResponse(self, message):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write(message)

def homePageMessage(self, message):
    data = {"message": message}
    self.response.headers['Content-Type'] = 'text/html'
    template = jinja_env.get_template('static/main_page.html')
    self.response.write(template.render(data))

class TermsPrivacyHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('static/terms_privacy.html')
        self.response.write(template.render())


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        homePageMessage(self, "WELCOME")

    def post(self):
        type = str(self.request.get('type'))

        if type == "login":
            logging.info("login")
            email = self.request.get('email')
            psw = self.request.get('psw')
            remember = self.request.get('remember')
            #plainTextResponse(self, "LOGIN QUERY: %s, %s, %s" % (uname, psw, remember))

            query = database.User.query(database.User.email == email, database.User.password == psw)
            results = query.fetch()

            if len(results) == 0:
                #plainTextResponse(self, "The combination of username and password does not exist")
                homePageMessage(self, "Those credentials were invalid. Try again.")

            else:
                user = results[0]
                #plainTextResponse(self, "You have logged in! User email is %s" % (user.email))
                homePageMessage(self, "You have logged in as user %s!" % (user.email))

        elif type == "signup":
            logging.info("signup")
            email = self.request.get('email')

            query = database.User.query(database.User.email == email)
            results = query.fetch()

            if len(results) > 0:
                #plainTextResponse(self, "This email is already taken.")
                homePageMessage(self, "This email is already taken. Try again.")

            else:
                psw = self.request.get('psw')
                psw_repeat = self.request.get('psw-repeat')

                if (psw == psw_repeat):
                    remember = self.request.get('remember')

                    newUser = database.User(email=email, password=psw)
                    newUser.put()

                    #plainTextResponse(self, "You have successfully signed up!")
                    homePageMessage(self, "You have successfully signed up!")
                else:
                    #plainTextResponse(self, "The passwords you entered are not the same.")
                    homePageMessage(self, "Your passwords didn't match. Try again.")


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/terms_privacy', TermsPrivacyHandler)
], debug=True)
