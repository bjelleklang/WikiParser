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
import sys
import os

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
            page = Page()
            
            event, root = self.context.next()
            register_nodes = False
            nodesreg = ""

            for event, element in self.context:
                ns, tag = string.split(element.tag, '}', 1)
                
                print element
                # Add startevent; if page append all data to var until event end
                if event == "start" and tag == "page":
                    register_nodes=True

                # Parse node only if it's a page
                if event == "end" and tag == "page":
                    page.parse(element)
                    register_nodes = False
                    print nodesreg
                    nodesreg = ""
                    root.clear()
                    sys.exit(0)

                nodesreg[len(nodesreg)] = element

            # Cleanup, logging stats
#            stats.log()
        except:
            traceback.print_exc()
            
        return True
        
 
class Page(object):
    def parse(self, page):
        ''' Parses a page. Will add page to pages.sql, and revisions to revs.sql.
            revs.sql will be split into multiple files according to what source file we use
        ''' 
        pagefile = "/media/tb/WikipediaDownloads/data"
        
        ns, tag = string.split(page.tag, '}', 1)
        pagetitle = page.find(ns + "}title")

        print pagetitle
        print ns
        print tag
        
    def log(self):
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
