'''
Created on Feb 7, 2013

@author: chris
'''

import xml.etree.ElementTree as xml

class XmlWrapper(object):
    '''
    classdocs
    '''
    xmldata = ""
    

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.xmldata = xml.parse(filename)    
        
        
    def searchNode(self, section, pattern):
        i=0
        root = self.xmldata.getroot()
        
        pages = root.findall("page")
        for p in pages:
            print i
            i=i+1
            
            if i> 10:
                break