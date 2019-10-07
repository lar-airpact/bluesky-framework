#!/bin/csh -f

#  Run BlueSky SMARTFIRE for EmissionFilesOnly for AIRPACT-5 Date, from 08Z  ##
#  Farren Herron-Thorpe April 10, 2014
#  Modified for Fire-SOA Project, Aug 07, 2017 
#  Usage: Fire-SOA_EFO_AP4.csh YYYYMMDD
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

#set TARGET_DIR  = /fastscratch/airpact5/AIRRUN/${YYYY}/${YYYYMMDD}00/EMISSION/fire/bluesky
#set LOG_DIR = /fastscratch/airpact5/AIRRUN/${YYYY}/${YYYYMMDD}00/LOGS

set TARGET_DIR  = /home/airpact5/projects/fire-soa_nt/fire_orl/transfer
set LOG_DIR     = /home/airpact5/projects/fire-soa_nt/fire_orl/transfer
#mkdir -v -p $TARGET_DIR 

set ORIGIN = $BS_DIR/output/${YYYYMMDD}00.1

# RUN BLUESKY after cleaning up the output space
rm -r -f $ORIGIN
date >> $LOG_DIR/bluesky_job.log
$BS_DIR/bluesky -d ${YYYYMMDD}00Z -K no-archive defaultLAR >> $LOG_DIR/bluesky_job.log
echo "BlueSky run complete" >>  $LOG_DIR/bluesky_job.log
date >> $LOG_DIR/bluesky_job.log

#Check if successful
if ( ! -e $ORIGIN/fire_locations.csv ) then
   echo "fire_locations.csv file not found; stopping fire processing"
   exit
endif

# NOW transfer output file to AIRPACT run directory

cp $ORIGIN/fire_locations.csv $BS_DIR/conversion/fire_locations.csv
cp $ORIGIN/summary.txt $BS_DIR/conversion/summary.txt
cd $BS_DIR/conversion

# NOW convert fire_locations.csv output to orl format SMOKE input using modified Pinder Code

fire_ptday.py
fire_ptinv.py
write_kml.py

mv $BS_DIR/conversion/fire_locations.kml $TARGET_DIR/fire_locations_${YYYYMMDD}.kml
mv $BS_DIR/conversion/fire_locations.csv $TARGET_DIR/
mv $BS_DIR/conversion/summary.txt $TARGET_DIR/
mv $BS_DIR/conversion/ptday.orl $TARGET_DIR/ptday-${YYYYMMDD}00.orl
mv $BS_DIR/conversion/ptinv.orl $TARGET_DIR/ptinv-${YYYYMMDD}00.orl

ls -al $TARGET_DIR
#Cleanup
rm -r -f $ORIGIN

echo END OF SCRIPT $0
exit ( $exitstat )

