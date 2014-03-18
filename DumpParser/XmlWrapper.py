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
import yaml

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
    ''' Misc counters and numLists for keeping track of everything '''
    pwithref = 0
    pworef = 0
    
    nscounts = {}
    articlestats = []
    titlechecks = []
    
    def parsePage(self, page):
        ''' Takes a page and does something to it. Is only called if the 
            page isn't a redirect, list, number, month, date or similar. ''
            ''' 
        
        # Ugly fix to include the namespace when searching for childnode. 
        # There just has to be a better way... 
        title = page.find(ns + "}title")
        revision = page.find(ns + "}revision")
        textNode = revision.find(ns + "}text")
        
        print page

        validArticle = True
        
          
    def incrNs(self, ns):
        ''' Increments the ns register, registers ns if not already done '''
        if ns not in self.nscounts:
            self.nscounts[ns] = 0
            
        self.nscounts[ns] = self.nscounts[ns] + 1
            
    
    
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
        
    def isDab(self, title):
        '''
            Checks the page title looking for (disambiguation) 
        '''
        
        if title.find("(disambiguation)") == -1:
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
        DataLogger.l("/tmp/wplog.txt", "Num redirects: " + str(self.numRedirects))
        DataLogger.l("/tmp/wplog.txt", "Num dabs: " + str(self.numDabs))
        DataLogger.l("/tmp/wplog.txt", "Num lists: " + str(self.numLists))
        DataLogger.l("/tmp/wplog.txt", "Num pages per ns: " + pprint.pformat(self.nscounts))
        DataLogger.l("/tmp/wplog.txt", "Avg length: " + pprint.pformat(self.lengthTotal / len(self.articlestats)))
        DataLogger.l("/tmp/wplog.txt", "Avg images per article: " + pprint.pformat(self.numImgsTotal / len(self.articlestats)))
        DataLogger.l("/tmp/wplog.txt", "Avg extlinks: " + pprint.pformat(self.numExtLinksTotal / len(self.articlestats)))
        DataLogger.l("/tmp/wplog.txt", "Avg wplinks: " + pprint.pformat(self.numLinksTotal / len(self.articlestats)))
        DataLogger.l("/tmp/wplog.txt", "Avg templates: " + pprint.pformat(self.numTemplatesTotal / len(self.articlestats)))
        
class PageData(object):
    length = 0
    numlinks = 0
    numtemplates = 0
    numextlinks = 0
    imagecount = 0
        
    def __init__(self, page):
        ''' 
            Simple constructor that looks for a ref and logs some stats about 
            this article. We ignore revisions for now, and only work with the 
            current rev. Later on, this should receive a number of revisions and 
            parse each of them, only checking for refs on the current rev. 
            
            We also assume that no numRedirects are passed into this constructor, 
            as the stats we are logging would be useless for those.  
        '''
        
        ns, tag = string.split(page.tag, '}', 1)
        
        title = page.find(ns + "}title")
        revision = page.find(ns + "}revision")
        textNode = revision.find(ns + "}text")
        
        # Parses the text and logs the article if it's missing a reftag or template
        t = textNode.text
        hasRef = self.hasRefTag(t)
        hasRefSection = self.hasRefSection(t)
        
        self.length = len(t)
        self.numlinks = len(re.findall('\[\[', t))
        self.numtemplates = len(re.findall('\{\{', t))
        
        # Regex for extlinks should be fixed and look for any single [ 
        # not preceded by another where alphanums follows.
        self.numextlinks = len(re.findall('\[\ ?(http|https|www)', t))
        self.imagecount = len(re.findall(r'\[\[(File|Image)\:', t))
        
        if hasRef == False:
            if hasRefSection == False:
                DataLogger.l("/tmp/wp_missing_norefsection.txt", "Missing: [[" + title.text + "]]")
            else:
                DataLogger.l("/tmp/wp_missing_refsection.txt", "Missing: [[" + title.text + "]]")
            
        
        
    def hasRefTag(self, aText):
        '''
            Receives the text of an article, lowercases everything and looks for 
            reftags
        '''
        try:
            aText = aText.strip().lower()
            if aText.find("<ref") == -1:
                return False
                
        except AttributeError:
            return True
        
        return True
    
