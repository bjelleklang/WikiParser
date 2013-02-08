'''
Created on Feb 7, 2013

@author: chris
'''


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
        f = open(logfile, 'a')
        
        f.write(data)
        f.close()