# Copyright 2018 Google LLC
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

# from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import logging

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

def email(recipient, subject, message):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # store = file.Storage('token.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    #     creds = tools.run_flow(flow, store)

    # BEGIN APPENGINE CREDENTIALS CODE
    filename = "token.json"
    file = open(filename, "r")

    jsonString = ""
    for line in file:
        jsonString += line

    # https://oauth2client.readthedocs.io/en/latest/source/oauth2client.client.html#oauth2client.client.Credentials
    creds = client.Credentials.new_from_json(jsonString)
    # END APPENGINE CREDENTIALS CODE

    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    message = create_message("windowlogindemo@gmail.com", recipient, subject, message)
    send_message(service, "me", message)

# [END gmail_quickstart]

from email.mime.text import MIMEText
import base64
from googleapiclient import errors

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    logging.info('Message Id: %s' % message['id'])
    return message
  except errors.HttpError, error:
    logging.info('An error occurred: %s' % error)
