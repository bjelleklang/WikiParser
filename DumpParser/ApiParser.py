'''
Created on Feb 19, 2013

@author: chris
'''
import httplib

class ApiParser(object):

    def __init__(self, pagename):
		conn = httplib.HTTPConnection("en.wikipedia.org")
		h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "PythonDev Chris chris@bjelleklang.org enwp User:Bjelleklang TEST ONLY"}
		conn.request("GET", "/w/api.php?format=xml&action=query&titles=Central%20Park&prop=revisions&rvprop=content", "", h)
		res = conn.getresponse()
		code = res.status
		data = res.read()		

			
