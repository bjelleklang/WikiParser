#!/usr/bin/python
import sys
import os
import time


'''
	Takes a text-file containing a tab-delimited list of users and generates sql to insert them.

	Todo: Strip file from param and use path for outputfile
'''

if len(sys.argv)!=2:
	print "Usage: loadusers.py <datafile>"
	exit()


timestarted = time.time()
infile = sys.argv[1]
headers = True

outfile = os.path.dirname(infile) + "/data/processed_user_file-"
outfileext = ".txt"

counter = 0
filesplitter = 0
f = open(infile, 'r')
of = open(outfile + "0" + outfileext, 'w')

inshead = "INSERT INTO user VALUES "

for line in f:
	data = line.split('\t')
	userid = data[0]
	username = data[1].replace("'", "\\'")
	regdate = data[2].replace("'", "\\'")

	ins = "('" + str(userid) + "','" + str(username) + "','" + str(regdate.strip()) + "')"
	of.write(ins + '\n')
	counter += 1

	if ((counter % 2) == 0):
		ins = ins + ";"
		of.write(ins + '\n')
		of.write(inshead + '\n')
	else:
		of.write(ins + '\n')


	if ((counter % 50000) == 0):		
		sys.stdout.write("%d users processed...    \r" % (counter) )
		sys.stdout.flush()

	if ((counter % 1000000) == 0):
		of.close()
		filesplitter += 1
		of = open(outfile + str(filesplitter) + outfileext, 'w')
	

timefinished = time.time()
totaltime = str((timefinished-timestarted))

print "%d users processed, all done.        \r" % (counter)
print "   Processing took %s seconds.     \r " % totaltime

of.close()
f.close();
