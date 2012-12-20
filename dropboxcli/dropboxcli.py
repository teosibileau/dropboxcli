#!/usr/bin/env python
import os
import sys
import settings
from dropbox import client, rest, session

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
TOKEN_FILE = os.path.join(SCRIPT_ROOT,'.access_token')

class Auth():
    def __init__(self):
        self.sess = session.DropboxSession(settings.APP_KEY, settings.APP_SECRET, settings.ACCESS_TYPE)
        try:
            with open(TOKEN_FILE, 'r') as token_file:
                for line in token_file:
                    s = line.split('-')
                    if s.__len__() == 2:
                        self.sess.set_token(s[0], s[1])
                    break
            self.client = client.DropboxClient(self.sess)
        except:
            request_token = self.sess.obtain_request_token()
            url = self.sess.build_authorize_url(request_token)
            print "url:", url
            print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
            raw_input()
            access_token = self.sess.obtain_access_token(request_token)
            with open(TOKEN_FILE, 'w') as token_file:
                token_file.write('%s-%s' % (access_token.key, access_token.secret))
                token_file.close()
            self.client = client.DropboxClient(self.sess)

def upload():
    args = sys.argv
    args.pop(0)
    path = os.getcwd()
    a = Auth()
    for arg in args:
        try:
            f = open(os.path.join(path,arg))
            response = a.client.put_file(arg,f)
            print "uploaded", response
        except Exception as e:
            print e

upload()
