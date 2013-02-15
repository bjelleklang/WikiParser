'''
Created on Feb 7, 2013

@author: chris
'''

from xml.etree.cElementTree import iterparse
from DataLogger import DataLogger
import string
import re
import pprint
import traceback
import pdb

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
        '''
            Iterates through a loop node looking for page nodes
        '''
        try:
            stats = LogStats()
            
            event, root = self.context.next()
           
             
            for event, element in self.context:
                ns, tag = string.split(element.tag, '}', 1)
    
                # Parse node only if it's a page
                if event == "end" and tag == "page":
                    stats.parsePage(element)
            
                    root.clear()


            # Cleanup, logging stats
            stats.log()
        except:
            traceback.print_exc()
            
        return True
        
 
class LogStats(object):
    ''' Misc counters and lists for keeping track of everything '''
    redirects = 0
    lists = 0
    comparisons = 0
    
    nscounts = {}
    articlestats = []
    titlechecks = []
    
    def __init__(self):
       # Ignorelists. Any article matching these regexes should be ignored
       # We don't need stats on these, as they are essentially a bunch of links
       self.titlechecks.append('^List\ ')
       self.titlechecks.append('^Comparison\ ')
       self.titlechecks.append('^(January|February|March|April|March|April|May|June|July|August|September|October|November|December)($|\ [0-9]{1,2}$)')
       self.titlechecks.append('^[0-9]{1,10}($|\ \(number\)$)') 
            
    def parsePage(self, page):
        ''' Takes a page and does something to it. Is only called if the 
            page isn't a redirect, list, number, month, date or similar. ''
            ''' 
        
        ns, tag = string.split(page.tag, '}', 1)
        
        # Ugly fix to include the namespace when searching for childnode. 
        # There just has to be a better way... 
        title = page.find(ns + "}title")
        revision = page.find(ns + "}revision")
        textNode = revision.find(ns + "}text")
        
        
        self.incrNs(page.find(ns + "}ns").text) 
        
        # Log redirects, parse page if it isn't one
        if self.isRedirect(textNode) == True:
            self.redirects = self.redirects + 1 
        elif self.isListLike(title.text) == True:
            self.lists = self.lists + 1
        else:
            # Parsing continues
            hasRef = self.hasRefTag(textNode.text)
            print hasRef
            if hasRef == False:
                DataLogger.l("/tmp/wperror.txt", "Missing: [[" + title.text + "]]")
          
    def incrNs(self, ns):
        ''' Increments the ns register, registers ns if not already done '''
        if ns not in self.nscounts:
            self.nscounts[ns] = 0
            
        self.nscounts[ns] = self.nscounts[ns] + 1
            
    def hasRefTag(self, aTextElem):
        
        try:
            aText = aTextElem.text
            aText = aText.strip().lower()
            status = "";
            if aText.find("<ref") == -1:
                return False
                
        except AttributeError:
            return True
        
        return True
    
    def isListLike(self, title):
        '''
            Checks the page title and compares it against the 
            regexes in titlechecks 
        '''
        #matched = re.match(self.titlechecks, title)
        combined = "(" + ")|(".join(self.titlechecks) + ")"
        
        if re.match(combined, title) == None:
            return False
        
        return True
    
    def isRedirect(self, aTextElem):
        '''
            Checks if a page contains a redirect
        '''
        try:
            aText = aTextElem.text
            aText = aText.strip().lower()
            status = "";
            if aText.startswith("#redirect") == False:
               return False
            
        except AttributeError:
            return True
        
        return True
    
    def log(self):
        DataLogger.l("/tmp/wplog.txt", "Num redirects: " + str(self.redirects))
        DataLogger.l("/tmp/wplog.txt", "Num lists: " + str(self.lists))
        DataLogger.l("/tmp/wplog.txt", "Num pages per ns: " + pprint.pformat(self.nscounts))
    
class PageData(object):
    length = 0
    numlinks = 0
    numextlinks = 0
    imagecount = 0
    
