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

def homePageMessage(self, loginMessage, signupMessage):
    if len(loginMessage) == 0:
        loginMessage = "Please fill in this form to login."
    if len(signupMessage) == 0:
        signupMessage = "Please fill in this form to create an account."

    data = {"loginMessage": loginMessage, "signupMessage": signupMessage}
    self.response.headers['Content-Type'] = 'text/html'
    template = jinja_env.get_template('static/main_page.html')
    self.response.write(template.render(data))

def successMessage(self, type):
    data = {"TYPE": type}
    self.response.headers['Content-Type'] = 'text/html'
    template = jinja_env.get_template('static/success.html')
    self.response.write(template.render(data))


class TermsPrivacyHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('static/terms_privacy.html')
        self.response.write(template.render())


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        cookie_value = self.request.cookies.get('login_cookie')
        if cookie_value == "":
            homePageMessage(self, "", "")
        else:
            all_users = database.User.query().fetch()
            user_entity = None
            for user in all_users:
                if str(user.key) == cookie_value:
                    user_entity = user
                    break

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

                # SEE COOKIE COMMENTS BELOW FOR SIGNUP SECTION
                datastore_key = str(user.put())
                self.response.set_cookie('login_cookie', value=datastore_key, path="/")

                #plainTextResponse(self, "You have logged in! User email is %s" % (user.email))
                #homePageMessage(self, "", "")
                #successMessage(self, "LOGIN")
                self.response.headers['Content-Type'] = 'text/html'
                template = jinja_env.get_template('static/login.html')
                self.response.write(template.render())

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

                    newUser = database.User(email=email, password=psw, listOfWords=[])
                    datastore_key = str(newUser.put())
                    #https://cloud.google.com/appengine/docs/standard/python/ndb/creating-entities

                    #self.response.set_cookie('login_cookie', key, path='/app',domain='website-login-demo.appspot.com', secure=True)
                    self.response.set_cookie('login_cookie', value=datastore_key, path="/")
                    #https://webapp2.readthedocs.io/en/latest/guide/response.html

                    #plainTextResponse(self, "You have successfully signed up!")
                    #homePageMessage(self, "", "You have successfully signed up!")
                    #successMessage(self, "SIGN UP")

                    import time
                    time.sleep(1)

                    self.response.headers['Content-Type'] = 'text/html'
                    template = jinja_env.get_template('static/login.html')
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
        all_users = database.User.query().fetch()
        user_entity = None
        for user in all_users:
            logging.info(str(user.key))
            if str(user.key) == cookie_value:
                user_entity = user
                break

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

        all_users = database.User.query().fetch()
        user_entity = None
        for user in all_users:
            if str(user.key) == cookie_value:
                user_entity = user
                break

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
        template = jinja_env.get_template('static/logout.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/terms_privacy', TermsPrivacyHandler),
    ('/logout', LogoutHandler),
    ('/app', AppHandler)
], debug=True)
