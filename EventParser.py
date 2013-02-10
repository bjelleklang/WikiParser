'''
Created on Feb 7, 2013

@author: chris
'''


class EventParser(object):
    def __init__(self):
        self.text = []
        
    def start(self, tag, attrib):
        self.is_title = True if tag == 'page' else False
    def end(self, tag):
        pass
    def data(self, data):
        if self.is_title:
            self.text.append(data.encode('utf-8'))
    def close(self):
        return self.text
        