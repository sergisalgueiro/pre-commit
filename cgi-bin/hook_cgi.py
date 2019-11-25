#!/usr/bin/python

# Import modules for CGI handling
import cgi
import json
import sys

no_commit_files = ['version.var', 'Hardware.hw']


def response(data_to_print):
    print("Content-type: text/html\n")
    print (data_to_print)
    sys.exit(0)


# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
service = form.getvalue('service')
author = form.getvalue('author')
project = form.getvalue('project')
organization = form.getvalue('organization')
youngest = form.getvalue('youngest')
log = form.getvalue('log')
changed = form.getvalue('changed')


# Sanity check
if log is None:
    data = json.dumps({"action": "deny", "reason": "The commit log message is empty."})
    response(data)

# if the commit contains the key string, do not lock it.
locked = 'I know what I\'m doing' not in log

if locked:
    # Trying to commit banned files
    if any(substring in changed for substring in no_commit_files):
        data = json.dumps({"action": "deny", "reason": "You are trying to commit dangerous files:  {}. Remove them from"
                           " commit,\n or type \"I know what I\'m doing\" in the commit message".format(no_commit_files)})
    else:
        # Success, proceed to commit
        data = json.dumps({"action": "allow"})
else:
    data = json.dumps({"action": "allow"})

response(data)
