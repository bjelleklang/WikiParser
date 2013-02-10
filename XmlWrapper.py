'''
Created on Feb 7, 2013

@author: chris
'''

from xml.etree.cElementTree import iterparse
from DataLogger import DataLogger
import string
import re

class XmlWrapper(object):
    '''
    Parses the xml-dump from Wikipedia. 
    iterparses the root element and only checks start events until a <page> is 
    found. Once we have a <page>, we also check the end event, in order to 
    analyze a specific article. 
    '''
    xmldata = ""
    context = ""
    
    titlechecks = []
    
    def __init__(self, filename):
        '''
        Constructor
        '''
        
        # Ignorelists. Any article matching these regexes should be ignored
        # We don't need stats on these, as they are essentially a bunch of links
        self.titlechecks.append('^List\ ')
        self.titlechecks.append('^Comparison\ ')
        self.titlechecks.append('^(January|February|March|April|March|April|May|June|July|August|September|October|November|December)($|\ [0-9]{1,2}$)')
        self.titlechecks.append('^[0-9]{1,10}($|\ \(number\)$)')
        
        
        self.context = iterparse( filename, events=("start", "end"))
        self.context = iter(self.context)
    
    def search(self):
        # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
        # Author: Liza Daly
        
        event, root = self.context.next()
        
        for event, element in self.context:
            ns, tag = string.split(element.tag, '}', 1)

            # Parse node only if it's a page
            if event == "end" and tag == "page":
                self.parsePage(element)
        
                root.clear()
        
        
    def parsePage(self, element):
        '''
            Parses a pagenode. 
            Will do a number of things based on the title, namespace and content
            of the page. 
        '''
        ns, tag = string.split(element.tag, '}', 1)
        
        # Ugly fix to include the namespace when searcin for childnode. 
        # There just has to be a better way... 
        title = element.find(ns + "}title")
        revision = element.find(ns + "}revision")
        textNode = revision.find(ns + "}text")
        
        
        
        if title.text.startswith("List") == False and wns.text == '0': 
            if self.doStuffToArticle(textNode.text, title.text) == False:
                #print "Logging: " + title.text
                DataLogger.l("/tmp/wplog.txt", "Missing: [[" + title.text + "]]")
    
    
    
    def doStuffToArticle(self, aText, title):
        '''
            Tries to find a reftag in the aText, and returns either true or false 
            based on the result. Also looks for #redirect in case the article is
            a redirect (which naturally doesnt contain any references)  
        '''
        
        try:
            aText = aText.strip().lower()
            status = "";
            if aText.find("<ref") == -1 and aText.startswith("#redirect") == False:
                return False
        except AttributeError:
            DataLogger.l("/tmp/wperror.txt", "Missing: [[" + title + "]]")
            return True
            
        return True
        
 
class LogStats(object):
    ''' Misc counters and lists for keeping track of everything '''
    redirects = 0
    lists = 0
    comparisons = 0
    nscounts = {}
    articlestats = []
    
    def parsePage(self, page):
        ''' Takes a page and does something to it. Is only called if the 
            page isn't a redirect, list, number, month, date or similar. ''' 
    
class PageData(object):
    length = 0
    numlinks = 0
    numextlinks = 0
    imagecount = 0
    
