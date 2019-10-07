#!/usr/bin/python
#
# this converts BlueSky fire info (fire_locations.csv) into ORL ptday SMOKE files for
# CMAQ inline fire plume rise
#
# Farren Herron-Thorpe 2016-06-23
# Serena Chung 2016-03-18
# Rob Pinder 2013-06-24
#    This version makes use of csv.DictReader so the column numbers do
#    not have to be hardwired into the code.

import csv

# Create ptday file

fout = open('./ptday.orl','w')
fout.write('#ORL FIREEMIS\n')
fout.write('#TYPE    Day-specific Point Source Inventory for FIRES\n')
fout.write('#COUNTRY US\n')
fout.write('#YEAR 2016\n')
fout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
fout.write('#DESC FIPS,FIREID,LOCID,SCC,DATA,DATE,DATAVALUE,BEGHOUR,ENDHOUR\n')

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
        area = row['area']
        scc = row['scc']
        date_time = row['date_time']
        location_id = latitude + longitude
        year = date_time[2:4]
        month = date_time[4:6]
        day = date_time[6:8]
        fire_date = month + '/' + day + '/' + year
        VEG = row['VEG']
        if VEG == '':
            VEG = 'Veg not defined'
        heat = row['heat']
        if heat == '':
            print 'ERROR: no heat value'
            heat = 8000
        PM25_emis = row['pm25']
        PM10_emis = row['pm10']
        CO_emis = row['co']
        NOx_emis = row['nox']
        NH3_emis = row['nh3']
        SO2_emis = row['so2']
        VOC_emis = row['voc']
        VOC_new = float(VOC_emis) * 3
        VOC_emis = str(format(VOC_new,'.3f'))
        
        beginHour = 0
        endHour = 23

        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'PM2_5', fire_date, PM25_emis, beginHour, endHour)
        fout.write(lineOut)
        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'PM10', fire_date, PM10_emis, beginHour, endHour)
        fout.write(lineOut)
        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'CO', fire_date, CO_emis, beginHour, endHour)
        fout.write(lineOut)
        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'NH3', fire_date, NH3_emis, beginHour, endHour)
        fout.write(lineOut)
        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'NOX', fire_date, NOx_emis, beginHour, endHour)
        fout.write(lineOut)
        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'SO2', fire_date, SO2_emis, beginHour, endHour)
        fout.write(lineOut)
        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'VOC', fire_date, VOC_emis, beginHour, endHour)
        fout.write(lineOut)
        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'HFLUX', fire_date, heat, beginHour, endHour)
        fout.write(lineOut)
        lineOut = '"%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s\n' % (fips, id, location_id, scc, 'ACRESBURNED', fire_date, area, beginHour, endHour)
        fout.write(lineOut)

fout.close()

