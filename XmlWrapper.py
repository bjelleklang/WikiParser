'''
Created on Feb 7, 2013

@author: chris
'''

from xml.dom.minidom import parse

class XmlWrapper(object):
    '''
    classdocs
    '''
    xml = ""
    

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.xml = parse(filename)    
        
        
    def searchNode(self, section, pattern):
        i=0
        for node in self.xml.getElementsByTagName('mediawiki'):
           if i > 10:
               break
           print node.nodeName
           i = i+1