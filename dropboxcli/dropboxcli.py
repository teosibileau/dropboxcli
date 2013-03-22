#!/usr/bin/env python
import os
import sys
import yaml
from dropbox import client, session

from termcolor import cprint

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
TOKEN_FILE = os.path.join(SCRIPT_ROOT, '.access_token')

LINE_LENGHT = 40


class Header(object):
    def __init__(self, text, color='white'):
        print '\n'
        CPRINT = lambda x: cprint(x, color)
        line = ''.join(['#' for i in range(LINE_LENGHT)])
        CPRINT(line)
        CPRINT('\t %s' % text)
        CPRINT(line)
        print '\n'


class SimpleLine(object):
    def __init__(self, text, color='white'):
        CPRINT = lambda x: cprint(x, color)
        CPRINT(text)

YAML = os.path.join(
    os.path.expanduser('~'),
    '.dropboxcli.yaml'
)


class Access(object):
    app_key = None
    app_secret = None
    access_type = 'app_folder'
    consolidated = False

    def __init__(self):
        try:
            f = file(YAML, mode='r')
            y = yaml.load(f)
            SimpleLine('Accessing yaml settings', 'cyan')
            self.app_key = y['access']['app_key']
            self.app_secret = y['access']['app_secret']
            self.access_type = y['access']['access_type']
            f.close()
            self.consolidated = True
        except:
            SimpleLine('cant find YAML settings, generating one', 'magenta')
            self.app_key = raw_input("Please enter your Dropbox APP_KEY: ")
            self.app_secret = raw_input("Please enter your Dropbox APP_SECRET: ")

        if not self.consolidated:
            f = file(YAML, mode='w+')
            y = {}
            y['access'] = {}
            y['access']['app_key'] = self.app_key
            y['access']['app_secret'] = self.app_secret
            y['access']['access_type'] = self.access_type
            yaml.dump(y, f, indent=4)
            f.close()


class Auth():
    def __init__(self):
        self.access = Access()
        self.sess = session.DropboxSession(
            self.access.app_key,
            self.access.app_secret,
            self.access.access_type
        )
        try:
            f = file(YAML, mode='r')
            y = yaml.load(f)
            s = y['access']['token'].split('-')
            if s.__len__() == 2:
                self.sess.set_token(s[0], s[1])
            f.close()
            self.client = client.DropboxClient(self.sess)
        except:
            request_token = self.sess.obtain_request_token()
            url = self.sess.build_authorize_url(request_token)
            SimpleLine("url: %s" % url, 'yellow')
            SimpleLine(
                "Please visit this website and press the 'Allow' button, then hit 'Enter' here.",
                'cyan'
            )
            raw_input()
            access_token = self.sess.obtain_access_token(request_token)
            f = file(YAML, mode='r')
            y = yaml.load(f)
            f.close()
            y['access']['token'] = '%s-%s' % (access_token.key, access_token.secret)
            f = file(YAML, mode='w+')
            yaml.dump(y, f, indent=4)
            f.close()
            self.client = client.DropboxClient(self.sess)


def upload():
    Header('Dropbox Uploader', 'cyan')
    args = sys.argv
    args.pop(0)
    path = os.getcwd()
    a = Auth()
    for arg in args:
        try:
            f = open(os.path.join(path, arg))
            response = a.client.put_file(arg, f)
            print "uploaded", response
        except Exception as e:
            print e


if __name__ == '__main__':
    upload()
