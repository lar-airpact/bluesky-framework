#!/bin/csh -f


#Check WF Season Variable
source /home/airpact5/AIRHOME/run_fastscratch/set_AIRPACT_fire_season.csh 
echo $SEASON
# Define directories
setenv BS_DIR /opt/bluesky/bluesky_3.5.1

cd $BS_DIR/conversion

# NOW convert fire_locations.csv output to orl format SMOKE input using modified Pinder Code

  fire_ptday_SFonly.py
  fire_ptinv_SFonly.py
  write_kml.py

exit

