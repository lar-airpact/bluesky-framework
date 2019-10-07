#!/usr/bin/python
# this converts BlueSky fire info into KML for AIRPACT5 webpage
# Created by Serena Chung, Jen Hinds,  and Farren Herron-Thorpe

import csv
import os

#SEASON will be set to 'WILDFIRE' or 'NON-WILDFIRE'
#season = os.environ["SEASON"]
#season = 'NON-WILDFIRE' # For testing, comment out the line above and uncomment this line


#Writing the kml file.
f = open('fire_locations.kml', 'w')
f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
f.write("<Document>\n")
f.write('<Style id="pilefire">\n')
f.write("<BalloonStyle>\n")
f.write("    <text>$[description]</text>\n")
f.write("</BalloonStyle>\n")
f.write("<IconStyle>\n")
f.write("   <scale>0.5</scale>\n")
f.write("   <Icon>\n")
f.write("      <href>http://www.clker.com/cliparts/u/q/Y/q/p/9/saddleyerhorse-hi.png</href>\n")
f.write("   </Icon>\n")
f.write("</IconStyle>\n")
f.write("</Style>\n")
f.write('<Style id="agfire">\n')
f.write("<BalloonStyle>\n")
f.write("    <text>$[description]</text>\n")
f.write("</BalloonStyle>\n")
f.write("<IconStyle>\n")
f.write("   <scale>0.5</scale>\n")
f.write("   <Icon>\n")
f.write("      <href>http://www.clker.com/cliparts/v/t/e/M/1/Q/green-fire-hi.png</href>\n")
f.write("   </Icon>\n")
f.write("</IconStyle>\n")
f.write("</Style>\n")
f.write('<Style id="airfire">\n')
f.write("<BalloonStyle>\n")
f.write("    <text>$[description]</text>\n")
f.write("</BalloonStyle>\n")
f.write("<IconStyle>\n")
f.write("   <scale>0.5</scale>\n")
f.write("   <Icon>\n")
f.write("      <href>http://satepsanone.nesdis.noaa.gov/pub/FIRE/HMS/png_logo/FireIcon.png</href>\n")
f.write("   </Icon>\n")
f.write("</IconStyle>\n")
f.write("</Style>\n")
f.write('<Style id="rxfire">\n')
f.write("<BalloonStyle>\n")
f.write("    <text>$[description]</text>\n")
f.write("</BalloonStyle>\n")
f.write("<IconStyle>\n")
f.write("   <scale>0.5</scale>\n")
f.write("   <Icon>\n")
f.write("      <href>http://www.clker.com/cliparts/u/T/e/i/e/G/blue-flame-hi.png</href>\n")
f.write("   </Icon>\n")
f.write("</IconStyle>\n")
f.write("</Style>\n")
f.write("<name>" + 'fire_locations.kml' +"</name>\n")
lastid = 'null'

#pile_fips_list = eval(open('./pile_fips_list.txt').read())

reader = csv.DictReader(open('./fire_locations.csv'))
for row in reader:
    country = row['country']
    state = row['state']
    fips = row['fips']
    if fips != '-9999':
      if state == 'CO' or state == 'AK' or state == 'AZ' or state == 'OR' or state == 'WA' or state == 'ID' or state == 'CA' or state == 'MT' or state == 'NV' or state == 'UT' or state == 'WY':
        SFid = row['id']
        id = SFid[7:21]
        event_id = row['event_id']
        latitude = row['latitude']
        longitude = row['longitude']
        long = float(row['longitude'])
        type = row['type']
        area = row['area']
        size = float(area) / 3 #Dividing by 3 since VIIRS is in HMS data for SMARTFIRE2 per Susan O'Neill
        if size < 1:
           area = str(format(size,'.3f'))
        if size < 10 and size >= 1:
           area = str(format(size,'.2f'))
        if size < 100 and size >= 10:
           area = str(format(size,'.1f'))
        if size >= 100:
           area = str(format(size,'.0f'))
        scc = row['scc']
        date_time = row['date_time']
        location_id = latitude + longitude
        year = date_time[2:4]
        month = date_time[4:6]
        day = date_time[6:8]
        fire_date = month + '/' + day + '/' + year

        if int(month) == 9:
           type = 'WF'
        
        VEG = row['VEG']
        if VEG == '':
           VEG = 'Unknown'
        if VEG == 'Urban':
           VEG = 'Unknown'
           type = 'Ag'

        #Reset to WF if env var still says WF   
        #if season == 'WILDFIRE':
        #   type = 'WF'


        #if fips in pile_fips_list and int(month) > 9:
        #   type = 'pile'


        URL = row['event_url']
        URLlist = 'http://128.208.123.111/smartfire/data/hms/fires/20' + year + month + day        
        beginHour = 0
        endHour = 23
        fire_name = type + ' Event' 
        if lastid != SFid:
          #if type == 'pile':
          #  f.write("   <Placemark>\n")
          #  f.write("       <name>" + fire_name + "</name>\n")
          #  f.write('           <description><![CDATA[<html lang="en"><b>BlueSky USA Details:</b><br><br> ' + event_id + '<br><br>' + area + ' acres (recalculated as pile burn)<br><br>' + 'Fuel: ' + VEG + '<br><br><a href="' + URL + '">View This Fire Report (if still available)</a><br><br><a href="' + URLlist + '">View All BlueSky USA Fire Reports</a></html>]]></description>\n')
          #  f.write("           <styleUrl>#pilefire</styleUrl>\n")  
          #  f.write("       <Point>\n")
          #  f.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
          #  f.write("       </Point>\n")
          #  f.write("   </Placemark>\n")
          if type == 'Ag':
            f.write("   <Placemark>\n")
            f.write("       <name>" + fire_name + "</name>\n")
            f.write('           <description><![CDATA[<html lang="en"><b>BlueSky USA Details:</b><br><br> ' + event_id + '<br><br>' + area + ' acres <br><br>' + 'Fuel: ' + VEG + ' (possible Ag. burn)<br><br><a href="' + URL + '">View This Fire Report (if still available)</a><br><br><a href="' + URLlist + '">View All BlueSky USA Fire Reports</a></html>]]></description>\n')
            f.write("           <styleUrl>#agfire</styleUrl>\n")  
            f.write("       <Point>\n")
            f.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
            f.write("       </Point>\n")
            f.write("   </Placemark>\n")
          if type == 'WF':
            f.write("   <Placemark>\n")
            f.write("       <name>" + fire_name + "</name>\n")
            f.write('           <description><![CDATA[<html lang="en"><b>BlueSky USA WildFire Details:</b><br><br> ' + event_id + '<br><br>' + area + ' acres<br><br>' + 'Fuel: ' + VEG + '<br><br><a href="' + URL + '">View This Fire Report (if still available)</a><br><br><a href="' + URLlist + '">View All BlueSky USA Fire Reports</a></html>]]></description>\n')
            f.write("           <styleUrl>#airfire</styleUrl>\n")  
            f.write("       <Point>\n")
            f.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
            f.write("       </Point>\n")
            f.write("   </Placemark>\n")
          if type == 'RX':
            f.write("   <Placemark>\n")
            f.write("       <name>" + fire_name + "</name>\n")
            f.write('           <description><![CDATA[<html lang="en"><b>BlueSky USA RX Fire Details:</b><br><br> ' + event_id + '<br><br>' + area + ' acres<br><br>' + 'Fuel: ' + VEG + '<br><br><a href="' + URL + '">View This Fire Report (if still available)</a><br><br><a href="' + URLlist + '">View All BlueSky USA Fire Reports</a></html>]]></description>\n')
            f.write("           <styleUrl>#rxfire</styleUrl>\n")
            f.write("       <Point>\n")
            f.write("           <coordinates>" + str(longitude) + "," + str(latitude) + "," + str() + "</coordinates>\n")
            f.write("       </Point>\n")
            f.write("   </Placemark>\n")
        lastid = SFid
f.write("</Document>\n")
f.write("</kml>\n")
f.close()
