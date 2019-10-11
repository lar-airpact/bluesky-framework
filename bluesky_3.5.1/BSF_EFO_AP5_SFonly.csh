#!/bin/csh -f

#  Run BlueSky SMARTFIRE for EmissionFilesOnly for AIRPACT-5 Date, from 08Z  ##
#  Farren Herron-Thorpe April 10, 2014
#  Joe Vaughan Oct 31, 2017  Updated to run stuff under run_day1 instead of run_fastscratch.
#  Usage: BSF_EFO_AP5_SFonly.csh YYYYMMDD
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

# Check WF Season Variable
# Changed from /home/airpact5/AIRHOME/run_ap5_day1/set_AIRPACT_fire_season.csh
# AIRPACT runs as "airpact5" user so better to use non hard-coded path
# this way we can easily test it ourselves as well since ~ is our home dir
source ~/AIRHOME/run_ap5_day1/set_AIRPACT_fire_season.csh 

# Define directories
setenv BS_DIR /bluesky/dist/bluesky/

# Changed from /home/airpact5/AIRHOME/run_ap5_day1/emis/fire_orl/transfer
# AIRPACT runs as "airpact5" user so better to use non hard-coded path
# this way we can easily test it ourselves as well since ~ is our home dir
set TARGET_DIR  = ~/AIRHOME/run_ap5_day1/emis/fire_orl/transfer

# Changed from /home/airpact5/AIRHOME/run_ap5_day1/emis/fire_orl/transfer
# AIRPACT runs as "airpact5" user so better to use non hard-coded path
# this way we can easily test it ourselves as well since ~ is our home dir
set LOG_DIR = ~/AIRHOME/run_ap5_day1/emis/fire_orl/transfer
#mkdir -v -p $TARGET_DIR 

set ORIGIN = $BS_DIR/output/${YYYYMMDD}00.1

# RUN BLUESKY after cleaning up the output space
date >> $LOG_DIR/bluesky_job.log
$BS_DIR/bluesky -d ${YYYYMMDD}00Z -K no-archive defaultLAR_SFonly >> $LOG_DIR/bluesky_job.log
echo "BlueSky run complete" >>  $LOG_DIR/bluesky_job.log
date >> $LOG_DIR/bluesky_job.log

#Check if successful
if ( ! -e $ORIGIN/fire_locations.csv ) then
   echo "fire_locations.csv file not found; stopping fire processing"
   exit
endif

# NOW transfer output file to AIRPACT run directory

cp $ORIGIN/fire_locations.csv $BS_DIR/conversion/output/fire_locations.csv
cp $ORIGIN/summary.txt $BS_DIR/conversion/output/summary.txt
cd $BS_DIR/conversion

# NOW convert fire_locations.csv output to orl format SMOKE input using modified Pinder Code

  python fire_ptday_SFonly_Zhang.py
  python fire_ptinv_SFonly_Zhang.py
  python write_kml.py

mv $BS_DIR/conversion/output/fire_locations.kml $TARGET_DIR/fire_locations_${YYYYMMDD}.kml
mv $BS_DIR/conversion/output/fire_locations.csv $TARGET_DIR/
mv $BS_DIR/conversion/output/summary.txt $TARGET_DIR/
mv $BS_DIR/conversion/output/ptday.orl $TARGET_DIR/ptday-${YYYYMMDD}00.orl
mv $BS_DIR/conversion/output/ptinv.orl $TARGET_DIR/ptinv-${YYYYMMDD}00.orl

ls -al $TARGET_DIR

#Cleanup
rm -r -f $ORIGIN

echo END OF SCRIPT $0
exit ( $exitstat )

