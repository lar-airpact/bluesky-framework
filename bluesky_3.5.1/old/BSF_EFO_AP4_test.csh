#!/bin/csh -f

#  Run BlueSky SMARTFIRE for EmissionFilesOnly for AIRPACT-4 Date, from 08Z  ##
#  Farren Herron-Thorpe April 10, 2014
#  Usage: BSF_EFO_AP4.csh YYYYMMDD
# initialize exit status
set exitstat = 0

# Check argument
if ( ! $#argv == 1 ) then
   echo 'Invalid argument. '
   echo "Usage $0 <yyyymmddhh>"
   set exitstat = 1
   exit ( $exitstat )
else
   set RUNDATE = $1
   set YYYY = `echo $1 | cut -c1-4`
   set   MM = `echo $1 | cut -c5-6`
   set   DD = `echo $1 | cut -c7-8`
   set YYYYMMDD = $1
endif
 
# Define directories
setenv BS_DIR /opt/bluesky/bluesky_3.5.1
set TARGET_DIR  = /data/airpact4/AIRRUN/${YYYYMMDD}00/EMISSION/fire/bluesky
set ORIGIN = $BS_DIR/output/${YYYYMMDD}00.1
# RUN BLUESKY after cleaning up the output space
rm -r -f $ORIGIN


$BS_DIR/bluesky -d ${YYYYMMDD}00Z -K no-archive defaultLAR
cp $ORIGIN/fire_locations.csv $TARGET_DIR/fire_locations_midnight.csv
rm -r -f $ORIGIN

echo END OF SCRIPT $0
exit ( $exitstat )

