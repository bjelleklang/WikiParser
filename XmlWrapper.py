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
    
    def __init__(self, filename):
        '''
        Constructor
        '''
        self.context = iterparse( filename, events=("start", "end"))
        self.context = iter(self.context)
    
    def search(self):
        # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
        # Author: Liza Daly
        i=0
        logFrq = 10000
        
        event, root = self.context.next()
        
        for event, element in self.context:
            ns, tag = string.split(element.tag, '}', 1)

            if event == "end" and tag == "page":
                self.handleEvent(element)
        
                root.clear()
                
            i = i+1
            
            if i % logFrq == 0:
                print "Artikkel no: " + str(i)
        
    def handleEvent(self, element):
        ns, tag = string.split(element.tag, '}', 1)
        
        # Ugly fix to include the namespace when searcin for childnode. 
        # There just has to be a better way... 
        title = element.find(ns + "}title")
        revision = element.find(ns + "}revision")
        textNode = revision.find(ns + "}text")
        
        
        #if self.doStuffToArticle(textNode.text) == False:
         #   print "Logging " + title.text + " has no refs"
        if title.text.startswith("List") == False: 
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
