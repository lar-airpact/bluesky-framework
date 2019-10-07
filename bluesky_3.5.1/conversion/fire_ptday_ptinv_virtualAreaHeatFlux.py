#!/usr/bin/python
#
# this converts BlueSky fire info (fire_locations.csv) into ORL ptday SMOKE files for
# CMAQ inline fire plume rise
#
# this module was updated to use BlueSky sensitivity runs which allows bypass of CONSUME and FEPS
# BlueSky setup ini file only uses SF2 and FCCS.  Emissions are calculated based on the xwalk files derived from sensitivity runs. 
#
# Farren Herron-Thorpe 2016-08-29
# Serena Chung 2016-03-18
# Rob Pinder 2013-06-24
# Note that this script multiples VOCs x 3 to deal with low VOC EFs in BlueSky and divides heat x 3 to deal with 
# the bug in SMOKE 3.5.1 which multiples heat x 3 when opening these ORL files for fire emissions.
#
#  Change: Vikram Ravi, 4/3/2018
#          Vikram Ravi, 7/20/2018
import csv
import math
import glob
from emissions_and_virtual_hflux_area import *

############################
# user input
ptday_file = 'ptday.orl'
ptinv_file = 'ptinv.orl'
SFireError = True # Smartfire error of overestimating area?
xwalk_data_base = '/opt/bluesky/bluesky_3.5.1/conversion'
xwalk_file_list = glob.glob('{}/xwalk*_adduff.csv'.format(xwalk_data_base))
locations = csv.DictReader(open('./fire_locations.csv'))

pollutantList = ['PM2_5', 'PM10', 'CO', 'NOX', 'NH3', 'VOC', 'SO2']
stateList     = ['WA', 'OR', 'ID', 'CA', 'NV', 'MT', 'UT', 'WY', 'AB', 'BC']
output_ptday  = pollutantList + ['HFLUX', 'ACRESBURNED'] # for output

###########################

virtual_data = Emissions_and_Virtual_Heat_Area(pollutants=pollutantList)
WF_Emissions, RX_Emissions = virtual_data.read_emissions(file_path_list=xwalk_file_list)
ptday = virtual_data.ptday_writer(ptday_file=ptday_file, country=country, year=year)
ptinv = virtual_data.ptinv_writer(ptinv_file=ptinv_file, country=country, year=year)

# loop over the data
for row in locations:

    # if consumption flaming in the input data, use the bluesky emissions and apply the virtual calculation of that
    if 'consumption_flaming' in row.keys():
        fireData = virtual_data.get_blueSky_data(irow=row, SFire_Error=SFireError)
    else: # use xwalk as a fallback approach
        fireData = virtual_data.get_xwalk_data(irow=row, WF_Emission=WF_Emissions, RX_Emission=RX_Emissions, SFire_Error=SFireError)

    if fireData is None: continue
    if fireData['fips'] != '-9999': 
        if fireData['state'] in stateList:
            # write pollutant data
            for pollutant in output_ptday: 
                if fireData[pollutant]:
                    lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fireData['fips'], 
                                                                                    fireData['fire_id'], 
                                                                                    fireData['location_id'], 
                                                                                    fireData['scc'], 
                                                                                    pollutant,
                                                                                    fireData['fire_date'], 
                                                                                    fireData[pollutant], 
                                                                                    fireData['begin_hour'], 
                                                                                    fireData['end_hour'])

                    ptday.write(lineOut)

            # write fire location data
            lineOut = '"%s", "%s", "%s", "%s", "%s", %s, %s, "%s", %s, %s\n' % (fireData['fips'],
                                                                                fireData['fire_id'], 
                                                                                fireData['location_id'], 
                                                                                fireData['scc'], 
                                                                                fireData['VEG'],
                                                                                fireData['latitude'], 
                                                                                fireData['longitude'], 
                                                                                fireData['NFDRSCODE'], 
                                                                                fireData['mat_burned'],
                                                                                fireData['HFLUX'])
            ptinv.write(lineOut)

# close the files
ptday.close()
ptinv.close()
