'''
Created on Feb 7, 2013

@author: chris
'''
import codecs

class DataLogger(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def l(logfile, data):    
        f = codecs.open(logfile, 'a', 'utf-8')
        
        f.write(data + '\n')
        f.close()