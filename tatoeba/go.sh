#!/bin/bash

# Dang.  At this time (5/20/2013) there are only 30 sentences in tatoeba which are both japanese and tagged OK.
# So, this project is pointless.

# The idea was to find a Japanese word I don't know, and be able to look up a trustworthy example sentence that contains it
# for addition to Anki.  But, unless it's one of those 30, well...

# 1/13/2014 it's up to 221

set -e

rm -f sentences.csv
rm -f tags.csv
rm -f links.csv
wget http://tatoeba.org/files/downloads/sentences.csv
wget http://tatoeba.org/files/downloads/tags.csv
wget http://tatoeba.org/files/downloads/links.csv

pcregrep "^\d+\s+(jpn|eng)" sentences.csv | sort > sentences-filtered.csv
mv -f sentences-filtered.csv sentences.csv

pcregrep "^\d+\s+OK$" tags.csv | sort > tags-filtered.csv
mv -f tags-filtered.csv tags.csv

./filter-ok.py sentences.csv tags.csv > filtered.csv
