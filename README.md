# demo-login
Demo account creation/login page using HTML/CSS/JS templates from <a href="https://www.w3schools.com/howto/default.asp">W3Schools</a>.

Signup Form: https://www.w3schools.com/howto/howto_css_signup_form.asp
</br>
Login Form: https://www.w3schools.com/howto/howto_css_login_form.asp
</br>
Home Page Layout: https://www.w3schools.com/w3css/tryw3css_templates_coming_soon.htm

# Live Site
<!-- https://website-login-demo.appspot.com/ -->
Offline temporarily, but will be back up soon!

# progress + next steps
<ol>
  <li>Forms and post method - DONE</li>
  <li>Password bullet points instead of char - DONE</li>
  <li>Site layout/structure + datastore - DONE</li>
  <li>Terms & Privacy page - DONE</li>
  <li>Server-generated Error checking - DONE</li>
  <li>Server-generated Error alerts - DONE</li>
  <li>HTML5-generated error checking + alerts - DONE</li>
  <li>Form submit on enter (without HTML5 errors checking) - DONE</li>
  <li>Form submit on enter (with HTML5 errors checking) - DONE</li>
  <li>Success page - DONE</li>
  <li>Form data carry through after failed attempt</li>
  <li>JS Client-generated Error checking (include password = password???)</li>
  <li>JS Client-generated Error alerts</li>
  <li>Password requirements -> length, etc.</li>
  <li>User Account page(s)</li>
  <li>Deploy to Cloud - DONE</li>
  <li>Gmail API - DONE</li>
  <li>Get GC key and send confirmation email - DONE</li>
  <li>Captcha</li>
  <li>Forgot Password</li>
  <li>More TBD</li>
</ol>

# login credentials
<ol>
  <li>Storing Cookie on user's computer after signup or login - DONE</li>
  <li>Requiring Cookie to view APP page - DONE</li>
  <li>App page - DONE</li>
  <li>Log out page that clears cookie value - DONE</li>
  <li>Log out page that goes home - DONE</li>
  <li>Different home page if logged in - DONE</li>
  <li>Remove cookie from sign up - DONE</li>
  <li>Create link to confirm account + create handler for access - DONE</li>
  <li>Datastore field (account_confirmed boolean), add condition to check - DONE</li>
  <li>Added urlSafe encryption from datastore - DONE</li>
  <li>Create unique session id's (that overwrite local cookies after new id created/time period up) instead of using same session id</li>
  <li>Ensure session id is unique by adding a user-unique string</li>
  <li>Accommodate logins from several computers at once by having list of current session id's in datastore</li>
  <li>Let a user log out of all other sessions (like gmail)</li>
  <li>Extra level of encryption -> in urgent/not urgent section</li>
  <li>Add message for session requests that are no longer active -> some type of redirect/login prompt/handling</li>
  <li>Have confirm emails expire after a period of time (datastore + handler code)</li>
  <li>Option to report (I didn't enter this email, erase account)</li>
</ol>

# email
<ol>
  <li>Gitignore for credentials.json and token.json - DONE</li>
  <li>Secret.py for hidden email address - DONE</li>
  <li>Created dedicated email - DONE</li>
  <li>Quickstart - DONE</li>
  <li>Changed scope, authorized email, + made test email method w/ Handler (locally) - DONE</li>
  <li>Appengine_config + vendored python lib (locally) - DONE</li>
  <li>Email ^^ setup tweaked so credentials can be read online (not locally) - DONE</li>
  <li>Send email after new user sign up - DONE</li>
</ol>

# urgent and not urgent todos
<ol>
<li>Deploy as test</li>
<li>Add extra encryption to key (cookie value, confirmation url) in hidden python file "secret.py"</li>
<li>Change cookie name + other cookie details (HTTPS secure)</li>
<li>Add comments to code</li>
<li>Figure out next steps</li>
<li>List out resources used</li>
<li>Clean datastore</li>
<li>TEST!</li>
</ol>
