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

import string
import csv

# Create ptinv file
fout = open('./ptinv.orl','w')
fout.write('#ORL FIRE\n')
fout.write('#TYPE Point Source Inventory for FIRES\n')
fout.write('#COUNTRY US\n')
fout.write('#YEAR 2018\n')
fout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
fout.write('#DESC FIPS,FIREID,LOCID,SCC,NAME,LAT,LON,NFDRSCODE,MATBURNED,HEATCONTENT\n')

WF_HEATdict = eval(open('./xwalk_WF_HEAT_adduff.csv').read())
RX_HEATdict = eval(open('./xwalk_RX_HEAT_adduff.csv').read())

locations = csv.DictReader(open('./fire_locations.csv'))

for row in locations:
    country = row['country']
    state = row['state']
    fips = row['fips']
    if fips != '-9999':
      if state == 'OR' or state == 'WA' or state == 'ID' or state == 'CA' or state == 'MT' or state == 'NV' or state == 'UT' or state == 'WY':
        SFid = row['id']
        id = SFid[7:21]
        event_id = row['event_id']
        latitude = row['latitude']
        longitude = row['longitude']
        date_time = row['date_time']
        area = float(row['area'])
        scc = row['scc']
        location_id = latitude + longitude
        NFDRSCODE = '-9'
        veg = row['VEG']
        if veg == '':
            veg = 'veg not defined'

        FCCS_ID = row['fccs_number']

        type = row['type']

#The WF and RX heat scale is non-linear, so the derived lookups are given below (within +/- 10% of BlueSky)
        if area >= 1001:
             WFhs = 149
             RXhs = 145
        if area < 1001:
             WFhs = 129
             RXhs = 145
        if area < 801:
             WFhs = 120
             RXhs = 123
        if area < 601:
             WFhs = 99
             RXhs = 96
        if area < 451:
             WFhs = 74
             RXhs = 77
        if area < 301:
             WFhs = 56
             RXhs = 64
        if area < 201:
             WFhs = 45
             RXhs = 56
        if area < 81:
             WFhs = 40
             RXhs = 48


        if type == 'WF':
          heat      = str(format(area / 3 * WFhs * float(WF_HEATdict[FCCS_ID]),'.3f'))

        if type == 'RX':
          heat      = str(format(area / 3 * RXhs * float(RX_HEATdict[FCCS_ID]),'.3f'))

        if heat == '':
            print 'ERROR: no heat value'
            heat = 8000

        material_burned = 0
        name = veg
                
        lineOut = '"%s", "%s", "%s", "%s", "%s", %s, %s, "%s", %s, %s\n' % (fips, id, location_id, scc, name, latitude, longitude, NFDRSCODE, material_burned, heat)
        fout.write(lineOut)
fout.close()
