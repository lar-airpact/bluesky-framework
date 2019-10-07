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

import csv

# Create ptday file

fout = open('./ptday.orl','w')
fout.write('#ORL FIREEMIS\n')
fout.write('#TYPE    Day-specific Point Source Inventory for FIRES\n')
fout.write('#COUNTRY US\n')
fout.write('#YEAR 2018\n')
fout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
fout.write('#DESC FIPS,FIREID,LOCID,SCC,DATA,DATE,DATAVALUE,BEGHOUR,ENDHOUR\n')

#Using the Add Duff to Grass/Other version of FCCS
WF_PM25dict = eval(open('./xwalk_WF_PM25_adduff.csv').read())
RX_PM25dict = eval(open('./xwalk_RX_PM25_adduff.csv').read())
WF_PM10dict = eval(open('./xwalk_WF_PM10_adduff.csv').read())
RX_PM10dict = eval(open('./xwalk_RX_PM10_adduff.csv').read())
WF_COdict   = eval(open('./xwalk_WF_CO_adduff.csv').read())
RX_COdict   = eval(open('./xwalk_RX_CO_adduff.csv').read())
WF_NOxdict = eval(open('./xwalk_WF_NOx_adduff.csv').read())
RX_NOxdict = eval(open('./xwalk_RX_NOx_adduff.csv').read())
WF_NH3dict = eval(open('./xwalk_WF_NH3_adduff.csv').read())
RX_NH3dict = eval(open('./xwalk_RX_NH3_adduff.csv').read())
WF_SO2dict = eval(open('./xwalk_WF_SO2_adduff.csv').read())
RX_SO2dict = eval(open('./xwalk_RX_SO2_adduff.csv').read())
WF_VOCdict = eval(open('./xwalk_WF_VOC_adduff.csv').read())
RX_VOCdict = eval(open('./xwalk_RX_VOC_adduff.csv').read())
WF_HEATdict = eval(open('./xwalk_WF_HEAT_adduff.csv').read())
RX_HEATdict = eval(open('./xwalk_RX_HEAT_adduff.csv').read())

pile_fips_list = eval(open('./pile_fips_list.txt').read())

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
        area = float(row['area'])
        scc = row['scc']
        date_time = row['date_time']
        location_id = latitude + longitude
        year = date_time[2:4]
        month = date_time[4:6]
        day = date_time[6:8]
        fire_date = month + '/' + day + '/' + year
        FCCS_ID = row['fccs_number']
        veg = row['VEG']
        if veg == '':
            veg = 'veg not defined'

        type = row['type']

        if fips in pile_fips_list and int(month) > 9:
           type = 'pile'

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
          PM25_emis = str(format(area * float(WF_PM25dict[FCCS_ID]),'.3f'))
          PM10_emis = str(format(area * float(WF_PM10dict[FCCS_ID]),'.3f'))
          CO_emis   = str(format(area * float(WF_COdict[FCCS_ID]),'.3f'))
          HEAT_emis = str(format(area * float(WF_HEATdict[FCCS_ID]),'.3f'))
          NOx_emis  = str(format(area * float(WF_NOxdict[FCCS_ID]),'.3f'))
          NH3_emis  = str(format(area * float(WF_NH3dict[FCCS_ID]),'.3f'))
          SO2_emis  = str(format(area * float(WF_SO2dict[FCCS_ID]),'.3f'))
          VOC_emis  = str(format(3 * area * float(WF_VOCdict[FCCS_ID]),'.3f'))
          heat      = str(format(area / 3 * WFhs * float(WF_HEATdict[FCCS_ID]),'.3f'))

        if type == 'RX':
          PM25_emis = str(format(area * float(RX_PM25dict[FCCS_ID]),'.3f'))
          PM10_emis = str(format(area * float(RX_PM10dict[FCCS_ID]),'.3f'))
          CO_emis   = str(format(area * float(RX_COdict[FCCS_ID]),'.3f'))
          NOx_emis  = str(format(area * float(RX_NOxdict[FCCS_ID]),'.3f'))
          NH3_emis  = str(format(area * float(RX_NH3dict[FCCS_ID]),'.3f'))
          SO2_emis  = str(format(area * float(RX_SO2dict[FCCS_ID]),'.3f'))
          VOC_emis  = str(format(3 * area * float(RX_VOCdict[FCCS_ID]),'.3f'))
          heat      = str(format(area / 3 * RXhs * float(RX_HEATdict[FCCS_ID]),'.3f'))

        if type == 'pile': #Emission factors assume 200 tons of pile burning per 46 acres reported by SMARTFIRE
          PM25_emis = str(format(area * 0.024,'.3f'))
          PM10_emis = str(format(area * 0.028,'.3f'))
          CO_emis   = str(format(area * 0.138,'.3f'))
          NOx_emis  = str(format(area * 0.007,'.3f'))
          NH3_emis  = str(format(area * 0.0001,'.3f'))
          SO2_emis  = str(format(area * 0.0002,'.3f'))
          VOC_emis  = str(format(area * 0.03,'.3f'))
          heat      = str(format(area / 3 * RXhs * float(RX_HEATdict[FCCS_ID]),'.3f'))

        if heat == '':
            print 'ERROR: no heat value'
            heat = 8000
        
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

