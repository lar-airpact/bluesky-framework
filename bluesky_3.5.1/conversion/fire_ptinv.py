#!/usr/bin/python
# this converts BlueSky fire info into ORL ptinv SMOKE files for
# CMAQ inline fire plume rise
#
# Farren Herron-Thorpe June 23, 2016
# Serena Chung, March 18, 2016
# Rob Pinder, June 24, 2013

import string
import csv

# Create ptinv file
fout = open('./ptinv.orl','w')
fout.write('#ORL FIRE\n')
fout.write('#TYPE Point Source Inventory for FIRES\n')
fout.write('#COUNTRY US\n')
fout.write('#YEAR 2016\n')
fout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
fout.write('#DESC FIPS,FIREID,LOCID,SCC,NAME,LAT,LON,NFDRSCODE,MATBURNED,HEATCONTENT\n')

reader = csv.DictReader(open('./fire_locations.csv'))
for row in reader:
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
        area = row['area']
        scc = row['scc']
        location_id = latitude + longitude
        NFDRSCODE = '-9'
        VEG = row['VEG']
        if VEG == '':
            VEG = 'Veg not defined'
        heat = row['heat']
        if heat == '':
            print 'ERROR: no heat value'
            heat = 8000
        material_burned = 0
        name = VEG
                
        lineOut = '"%s", "%s", "%s", "%s", "%s", %s, %s, "%s", %s, %s\n' % (fips, id, location_id, scc, name, latitude, longitude, NFDRSCODE, material_burned, heat)
        fout.write(lineOut)
fout.close()

