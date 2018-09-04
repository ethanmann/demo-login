import webapp2
import logging
import jinja2
import os
import database
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def plainTextResponse(self, message):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write(message)

def homePageMessage(self, loginMessage, signupMessage):
    if len(loginMessage) == 0:
        loginMessage = "Please fill in this form to login."
    if len(signupMessage) == 0:
        signupMessage = "Please fill in this form to create an account."

    data = {"loginMessage": loginMessage, "signupMessage": signupMessage}
    self.response.headers['Content-Type'] = 'text/html'
    template = jinja_env.get_template('static/main_page.html')
    self.response.write(template.render(data))

# def successMessage(self, type):
#     data = {"TYPE": type}
#     self.response.headers['Content-Type'] = 'text/html'
#     template = jinja_env.get_template('static/success.html')
#     self.response.write(template.render(data))

class TermsPrivacyHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('static/terms_privacy.html')
        self.response.write(template.render())


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        cookie_value = self.request.cookies.get('login_cookie')
        if cookie_value == "" or cookie_value == None:
            homePageMessage(self, "", "")
        else:
            key_object = ndb.Key(urlsafe=cookie_value)
            user_entity = key_object.get()
            # all_users = database.User.query().fetch()
            # user_entity = None
            # for user in all_users:
            #     if str(user.key) == cookie_value:
            #         user_entity = user
            #         break

            self.response.headers['Content-Type'] = 'text/html'
            template = jinja_env.get_template('static/main_page_cookie.html')
            self.response.write(template.render({"email": user_entity.email}))

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
                homePageMessage(self, "Those credentials were invalid. Try again.", "")

            else:
                user = results[0]
                if user.emailConfirmed:
                    #https://cloud.google.com/appengine/docs/standard/python/ndb/creating-entities
                    #https://cloud.google.com/appengine/docs/standard/python/datastore/entities#Python_Understanding_write_costs
                    #SHOULD MINIMIZE # OF PUT OPERATIONS

                    datastore_key = user.key.urlsafe()
                    self.response.set_cookie('login_cookie', value=datastore_key, path="/")
                    #self.response.set_cookie('login_cookie', key, path='/app',domain='website-login-demo.appspot.com', secure=True)
                    #https://webapp2.readthedocs.io/en/latest/guide/response.html

                    #plainTextResponse(self, "You have logged in! User email is %s" % (user.email))
                    #homePageMessage(self, "", "")
                    #successMessage(self, "LOGIN")
                    self.response.headers['Content-Type'] = 'text/html'
                    template = jinja_env.get_template('static/script.html')
                    self.response.write(template.render({"location":"/app"}))

                else:
                    homePageMessage(self, "You still need to confirm your account. Check your email for a link.", "")

        elif type == "signup":
            logging.info("signup")
            email = self.request.get('email')

            query = database.User.query(database.User.email == email)
            results = query.fetch()

            if len(results) > 0:
                #plainTextResponse(self, "This email is already taken.")
                homePageMessage(self, "", "This email is already taken. Try again.")

            else:
                psw = self.request.get('psw')
                psw_repeat = self.request.get('psw-repeat')

                if (psw == psw_repeat):
                    remember = self.request.get('remember')

                    newUser = database.User(email=email, password=psw, listOfWords=[], emailConfirmed=False)
                    datastore_key = newUser.put().urlsafe()

                    #https://cloud.google.com/appengine/docs/standard/python/ndb/creating-entities

                    #plainTextResponse(self, "You have successfully signed up!")
                    #homePageMessage(self, "", "You have successfully signed up!")
                    #successMessage(self, "SIGN UP")

                    # import time
                    # time.sleep(1)


                    import email_methods
                    link = self.request.application_url + "/confirm?key=" + datastore_key
                    #https://docs.pylonsproject.org/projects/webob/en/stable/
                    email_methods.email(email, "Website Login Demo - Account Confirmation", "Click here to confirm your account: %s" % link)


                    self.response.headers['Content-Type'] = 'text/html'
                    template = jinja_env.get_template('static/confirmation_sent.html')
                    self.response.write(template.render())

                else:
                    #plainTextResponse(self, "The passwords you entered are not the same.")
                    homePageMessage(self, "", "Your passwords didn't match. Try again.")


class AppHandler(webapp2.RequestHandler):
    def get(self):
        #https://webapp2.readthedocs.io/en/latest/guide/request.html
        cookie_value = self.request.cookies.get('login_cookie')
        logging.info(cookie_value)

        if cookie_value == None or cookie_value == "":
            return webapp2.redirect('/')

        #https://cloud.google.com/appengine/docs/standard/python/ndb/creating-entities
        key_object = ndb.Key(urlsafe=cookie_value)
        user_entity = key_object.get()
        # all_users = database.User.query().fetch()
        # user_entity = None
        # for user in all_users:
        #     if str(user.key) == cookie_value:
        #         user_entity = user
        #         break
        logging.info(user_entity)

        data = {}
        data["listOfWords"] = user_entity.listOfWords
        data["email"] = user_entity.email

        #WILL NEED TO QUERY DATASTORE TO GET THE COOKIE-KEY
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('static/app.html')
        self.response.write(template.render(data))

    def post(self):
        new_word = self.request.get('new_word')
        clear = self.request.get('clear')

        cookie_value = self.request.cookies.get('login_cookie')
        logging.info(cookie_value)

        key_object = ndb.Key(urlsafe=cookie_value)
        user_entity = key_object.get()
        # all_users = database.User.query().fetch()
        # user_entity = None
        # for user in all_users:
        #     if str(user.key) == cookie_value:
        #         user_entity = user
        #         break

        if clear == "YES":
            user_entity.listOfWords = []
            user_entity.put()

        else:
            user_entity.listOfWords.append(new_word)
            user_entity.put()

        AppHandler.get(self)


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("LOGOUT GET")
        self.response.set_cookie('login_cookie', value="", path="/")

        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('static/script.html')
        self.response.write(template.render({"location":"/"}))

class ConfirmHandler(webapp2.RequestHandler):
    def get(self):
        key = self.request.get('key')
        # self.response.set_cookie('login_cookie', value=key, path="/")
        # Doesn't set cookie to force user to log in -> security

        if key == None or key == "":
            self.response.headers['Content-Type'] = 'text/html'
            template = jinja_env.get_template('static/confirmation_received.html')
            self.response.write(template.render())

        else:
            key_object = ndb.Key(urlsafe=key)
            user_entity = key_object.get()
            # all_users = database.User.query().fetch()
            # user_entity = None
            # for user in all_users:
            #     if str(user.key) == key:
            #         user_entity = user
            #         break

            user_entity.emailConfirmed = True
            user_entity.put()

            return webapp2.redirect('/confirm')
            #This masks the url from the user


# class TestHandler(webapp2.RequestHandler):
#     def get(self):
#         import secret
#         import email_methods
#
#         email_methods.email(secret.my_email, "TEST SUBJECT", "TEST MESSAGE TEXT")

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/terms_privacy', TermsPrivacyHandler),
    ('/logout', LogoutHandler),
    ('/confirm', ConfirmHandler),
    #('/test', TestHandler),
    ('/app', AppHandler)
], debug=True)
