#!/usr/bin/python

import httplib
import xml.etree.ElementTree as etree 
import traceback
from Db import Db

class CatWatcher(object):
    articlesInCat = 0
    
    def __init__(self):
        '''
        Constructor
        '''
        cat = "Pending%20AfC_submissions"
        
        xmldata = self.getCat(cat)
        print xmldata
        
        xmltree = etree.fromstring(xmldata)
        result = self.getPages(xmltree)
        self.updateDb(self.articlesInCat)
    
    def getCat(self, pagename):
        lk = "/w/api.php?action=query&format=xml&list=allcategories&aclimit=1&acprop=size&acfrom=" + pagename.replace(" ", "_")

        print lk
        print " "
        conn = httplib.HTTPConnection("en.wikipedia.org")
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "PythonDev Chris chris@bjelleklang.org enwp User:Bjelleklang TEST ONLY"}
        conn.request("GET", lk, "", h)
        res = conn.getresponse()
        code = res.status
        data = res.read()

        return data
        
    def getPages(self, xmltree):
        try:
            #stats = LogStats()
            
            for cm in xmltree.iter('c'):
                self.articlesInCat = cm.get("pages")

            # Cleanup, logging stats
            #stats.log()
        except:
            traceback.print_exc()
            
        return True
    
    def updateDb(self, count):
        sql = "INSERT INTO catPendCounts (cnt) VALUES (?)"
        
        db = oursql.connect(db='u_bjelleklang',
            host="sql",
            read_default_file=os.path.expanduser("~/.my.cnf"),
            charset=None,
            use_unicode=False
        )

        cursor = db.cursor()
        cursor.execute(sql, count)
        cursor.execute("commit")
        cursor.close()
        
    
ddd = CatWatcher()    
print ddd.articlesInCat