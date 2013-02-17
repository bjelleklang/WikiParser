#!/usr/local/bin/python2.7
# encoding: utf-8
'''
WikiParser -- Simple tool to parse MediaWiki XML

Parses an XMLdump from MediaWiki and looks in a given node for a specified 
regexp. A simple switch tells the tool to log all article names where the regexp 
is found (or the other way around). 

It defines classes_and_methods

@author:     user_name
        
@copyright:  2013 organization_name. All rights reserved.
        
@license:    BSD License

@contact:    chris@bjelleklang.org
@deffield    updated: Updated
'''

import sys
import os
import time 
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from XmlWrapper import XmlWrapper
import traceback


__all__ = []
__version__ = 0.1
__date__ = '2013-02-07'
__updated__ = '2013-02-07'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Christoffer Hafsahl on %s.
  Copyright 2013 Christoffer Hafsahl. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    starttime = time.clock()

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-f", "--file", dest="xmlfile", action="store", help="set the XML-file to parse", required=True)
        #parser.add_argument("-p", "--pattern", dest="pattern", action="store", help="set the regex you are looking for", required=True)
        #parser.add_argument("-s", "--section", dest="section", action="store", help="the section you want to look within", required=True)
       
        # Process arguments
        args = parser.parse_args()
        
        verbose = args.verbose
        hasError = False
        
        if verbose > 0:
            print("Verbose mode on")
        
        if os.path.isfile(args.xmlfile) != True :
            hasError = True
            print "The XML file doesn't exist"
        
        
        if hasError == False:
            wrapper = XmlWrapper(args.xmlfile)
            wrapper.search();
            
            
        print "Time elapsed: " + str(time.clock() - starttime)
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'WikiParser_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
