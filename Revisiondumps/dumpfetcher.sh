#!/bin/bash

prefix="http://dumps.wikimedia.org/enwiki/latest/"

outputdir=$1

declare -a sources=("enwiki-latest-stub-meta-history.xml.gz"
"enwiki-latest-stub-meta-history1.xml.gz"
"enwiki-latest-stub-meta-history10.xml.gz"
"enwiki-latest-stub-meta-history11.xml.gz"
"enwiki-latest-stub-meta-history12.xml.gz"
"enwiki-latest-stub-meta-history13.xml.gz"
"enwiki-latest-stub-meta-history14.xml.gz"
"enwiki-latest-stub-meta-history15.xml.gz"
"enwiki-latest-stub-meta-history16.xml.gz"
"enwiki-latest-stub-meta-history17.xml.gz"
"enwiki-latest-stub-meta-history18.xml.gz"
"enwiki-latest-stub-meta-history19.xml.gz"
"enwiki-latest-stub-meta-history2.xml.gz"
"enwiki-latest-stub-meta-history20.xml.gz"
"enwiki-latest-stub-meta-history21.xml.gz"
"enwiki-latest-stub-meta-history22.xml.gz"
"enwiki-latest-stub-meta-history23.xml.gz"
"enwiki-latest-stub-meta-history24.xml.gz"
"enwiki-latest-stub-meta-history25.xml.gz"
"enwiki-latest-stub-meta-history26.xml.gz"
"enwiki-latest-stub-meta-history27.xml.gz"
"enwiki-latest-stub-meta-history3.xml.gz"
"enwiki-latest-stub-meta-history4.xml.gz"
"enwiki-latest-stub-meta-history5.xml.gz"
"enwiki-latest-stub-meta-history6.xml.gz"
"enwiki-latest-stub-meta-history7.xml.gz"
"enwiki-latest-stub-meta-history8.xml.gz"
"enwiki-latest-stub-meta-history9.xml.gz")

if [ $# -eq 0 ] 
then
	echo "Usage: dumpfetcher.sh <output directory>"
	exit 1
fi

cd $outputdir

for i in "${sources[@]}"
do
	echo "Fetching $prefix$i"
	/usr/bin/wget "-c" $prefix$i
done
