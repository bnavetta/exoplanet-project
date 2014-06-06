#!/bin/sh

# http://archive.stsci.edu/cgi-bin/mastpreview?mission=hst&dataid=O8EX05010

curl -L -o hstonline_08EX05010.tar 'http://archive.stsci.edu/cgi-bin/mast_retrieve?mission=hstonline&hstonline_mark=O8EX05010'
tar xvf hstonline_08EX05010.tar
mv hstonline hstonline_08EX05010
