#!/bin/csh -f

# TEST_BSF.csh
#  Run test that bluesky code is found on bluesky server.  
#	JKv August 29, 2016

# Define directories
setenv BS_DIR /opt/bluesky/bluesky_3.5.1

echo TEST_BSF.csh tests accessability of bluesky executable on bluesky server.

 ls -lt $BS_DIR/bluesky 

echo END OF SCRIPT $0
exit

