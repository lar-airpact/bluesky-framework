#!/usr/bin/python
#
# this converts BlueSky fire info (fire_locations.csv) into ORL ptday SMOKE files for
# CMAQ inline fire plume rise
#
# this module was updated to use BlueSky sensitivity runs which allows bypass of CONSUME and FEPS
# BlueSky setup ini file only uses SF2 and FCCS.  Emissions are calculated based on the xwalk files derived from sensitivity runs.
#
# Farren Herron-Thorpe 2016-08-29
# Wei Zhang 2017-08-01 - used IEDQ method to calculate virtual heat and virtual area
# Serena Chung 2016-03-18
# Rob Pinder 2013-06-24
# Note that this script divides heat x 3 to deal with the bug in SMOKE 3.5.1 which multiples heat x 3 when opening these ORL files for fire emissions.

import string
import csv
import math

# calculate plume class based on DEASCO3
def getPlumeClass(flame_consumption, area):
     fpci = flame_consumption / math.sqrt(area)
     if fpci <= 75:
          return 1
     elif fpci <= 300:
          return 2
     elif fpci <= 675:
          return 3
     elif fpci <= 1250:
          return 4
     else:
          return 5
     
#Start Main Body     
layer1Fracts = { }
layer1Fracts[1] = 0.711
layer1Fracts[2] = 0.572
layer1Fracts[3] = 0.467
layer1Fracts[4] = 0.467
layer1Fracts[5] = 0.467

# Create ptinv file
fout = open('./ptinv.orl','w')
fout.write('#ORL FIRE\n')
fout.write('#TYPE Point Source Inventory for FIRES\n')
fout.write('#COUNTRY US\n')
fout.write('#YEAR 2016\n')
fout.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
fout.write('#DESC FIPS,FIREID,LOCID,SCC,NAME,LAT,LON,NFDRSCODE,MATBURNED,HEATCONTENT\n')

WF_HEATdict = eval(open('./xwalk_WF_HEAT_adduff.csv').read())
RX_HEATdict = eval(open('./xwalk_RX_HEAT_adduff.csv').read())

#Using flaming consumption lookups
WF_CONSFdict = eval(open('./xwalk_WF_cons_flam.csv').read())
RX_CONSFdict = eval(open('./xwalk_RX_cons_flam.csv').read())

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
        year = date_time[2:4]
        month = date_time[4:6]
        day = date_time[6:8]
        area = float(row['area'])
        scc = row['scc']
        location_id = latitude + longitude
        NFDRSCODE = '-9'
        veg = row['VEG']
        if veg == '':
            veg = 'veg not defined'

        FCCS_ID = row['fccs_number']

        type = row['type']

        if int(month) == 9:
           type = 'WF'

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
          heat = str(format(area / 3 * WFhs * float(WF_HEATdict[FCCS_ID]),'.3f'))
          conf = float(WF_CONSFdict[FCCS_ID])
        
        if type == 'RX':
          heat = str(format(area / 3 * RXhs * float(RX_HEATdict[FCCS_ID]),'.3f'))
          conf = float(RX_CONSFdict[FCCS_ID])
		  
        if heat == '':
            print 'ERROR: no heat value'
            heat = 8000

		# generate virtual area and virtual heat
        # virtual area is based on layer 1 fraction from WRAP/DEASCO3 and smoldering fraction formula in SMOKE
        flame_consumption = conf * area
        plume_class = getPlumeClass(flame_consumption, area)
        s_fract = layer1Fracts[plume_class]     
        virtual_area_layer1Fract = math.exp((1 - 0.3 - s_fract) / 0.0703)
        ## virtual_heat_layer1Fract_3 : 
        ## inspired by DEASCO3 Flaming Phase Consumption Index equation
        ## [virtual heat content] = [maximum flaming phase heat] / [square root of area]
        ## [maximum flaming phase heat] = consumption (tons/acre) * Area(Acres) * 16,000,000 (BTU/Ton)
        maximum_heat = conf  * area * 16000000
        virtual_heat_layer1Fract_3 = maximum_heat / math.sqrt(area)
     
        ## virtual_heat_layer1Fract_4 : 
        ## produce virtual heat content as follows 
        ## 1. area >=1001,  [Maximum flaming phase Heat] / [Square root of area]
        ## 2. area <= 1, [Maximum flaming Heat]
        ## 3. area between 1 and 1001, linear scale gradually from ([Maximum flaming phase Heat] / [Square root of area]) to ([Maximum flaming Heat])
        virtual_heat_layer1Fract_4 = 0
        if area < 1001:
              virtual_heat_layer1Fract_4 = virtual_heat_layer1Fract_3 + (maximum_heat - virtual_heat_layer1Fract_3) * (1001.0 - area) / 1000.0
        else:
              virtual_heat_layer1Fract_4 = virtual_heat_layer1Fract_3

        ## reduce heat by 3 times to compensate a bug in SMOKE (smkinven) process for SMOKE 3.5.1 (confirmed by SMOKE developer)
        virtual_heat = virtual_heat_layer1Fract_4 / 3.0
        virtual_area = virtual_area_layer1Fract	
			
        material_burned = 0
        name = veg
                
        lineOut = '"%s", "%s", "%s", "%s", "%s", %s, %s, "%s", %s, %s\n' % (fips, id, location_id, scc, name, latitude, longitude, NFDRSCODE, material_burned, virtual_heat)
        fout.write(lineOut)
fout.close()
