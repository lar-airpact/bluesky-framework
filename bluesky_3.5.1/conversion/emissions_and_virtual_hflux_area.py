import math
import os

class Emissions_and_Virtual_Heat_Area():
    def __init__(self, pollutants):
        self.pollutants = pollutants 

   # calculate plume class based on DEASCO3
    def _get_plume_class(self, flame_consumption=None, area=None):
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

    #The WF and RX heat scale is non-linear, so the derived lookups are given below (within +/- 10% of BlueSky)
    def get_heat_scale(self, area=None):
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
        return WFhs, RXhs

    def _get_virtual_area_heat(self, conf=None, area=None):
       layer1Fracts = {1:0.711, 2:0.572, 3:0.467, 4:0.467, 5:0.467 }
       
       # generate virtual area and virtual heat
       # virtual area is based on layer 1 fraction from WRAP/DEASCO3 and smoldering fraction formula in SMOKE
       flame_consumption = conf * area
       plume_class = self._get_plume_class(flame_consumption, area)
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
       virtual_heat_area = {'heat':virtual_heat, 'area':virtual_area}
    
       return virtual_heat_area

    def _get_xwalk_fileName(self, fileNameList=None, pollutant=None, WF_or_RX=None):
       for fileName in fileNameList:
           if WF_or_RX in fileName and pollutant in fileName:
               return fileName

    def read_emissions(self, file_path_list=None):
       
       WF_Emissions = dict.fromkeys( self.pollutants )
       RX_Emissions = dict.fromkeys( self.pollutants )
       
       #Using the Add Duff to Grass/Other version of FCCS
       for pollutantName in self.pollutants:
           #WF_fileName = './xwalk_{}_{}_adduff.csv'.format('WF', pollutantName)
           WF_fileName = self._get_xwalk_fileName(fileNameList=file_path_list, pollutant=pollutantName, WF_or_RX='WF') #'{}'.format( file_path_dict['WF'][pollutantName] )
           #RX_fileName = './xwalk_{}_{}_adduff.csv'.format('RX', pollutantName)
           RX_fileName = self._get_xwalk_fileName(fileNameList=file_path_list, pollutant=pollutantName, WF_or_RX='RX')
           try:
               WF_Emissions[pollutantName] = eval(open(WF_fileName).read())
           except:
               if not os.path.exists(WF_fileName):
                   print ("Input file not found: {} ".format(WF_fileName))
           try:
               RX_Emissions[pollutantName] = eval(open(RX_fileName).read())
           except:
               if not os.path.exists(RX_fileName):
                   print ("Input file not found: {} ".format(RX_fileName))
   
       #Using flaming consumption lookups
       WF_Emissions['Consumption_Flame'] = eval(open('./xwalk_WF_cons_flam.csv').read())
       RX_Emissions['Consumption_Flame'] = eval(open('./xwalk_RX_cons_flam.csv').read())

       return WF_Emissions, RX_Emissions
      
    def _formatter(self, x):
        x = float(x)
        return str(format( x, '.3f' ))

    def _dateFormatter(self, my_date):
        my_year  = my_date[2:4]
        my_month = my_date[4:6]
        my_day   = my_date[6:8]
        return my_month + '/' + my_day + '/' + my_year

    def _fire_information(self, irow=None):
        fire_info = dict.fromkeys(['country', 'state', 'fips', 'fire_id', 'location_id', 'scc', 'fire_date', 'NFDRSCODE', 'VEG', 'begin_hour', 'end_hour'])
        fire_info['country']     = irow['country']
        fire_info['state']       = irow['state']
        fire_info['fire_id']     = irow['id'][7:21]
        fire_info['location_id'] = irow['latitude'] + irow['longitude']
        fire_info['latitude']    = self._formatter(irow['latitude'])
        fire_info['longitude']   = self._formatter(irow['longitude'])
        fire_info['scc']         = irow['scc']
        fire_info['fire_date']   = self._dateFormatter(irow['date_time'])
        fire_info['begin_hour']  = 0
        fire_info['end_hour']    = 23
        fire_info['NFDRSCODE']   = '-9'
        fire_info['mat_burned']  = 0

        if 'VEG' in irow.keys():
            if irow['VEG']:
                fire_info['VEG'] = irow['VEG']
            else:
                fire_info['VEG'] = 'Vegetation not defined'
        else:
            fire_info['VEG'] = 'Vegetation not defined'

        if fire_info['country'].upper() == "USA":
            fire_info['fips']   = irow['fips']
        elif fire_info['country'].upper() == "CANADA":
            if fire_info['state'] == 'AB': 
                fire_info['fips'] = 48001
            elif fire_info['state'] == 'BC':
                fire_info['fips'] = 59001
            else:
                fire_info['fips'] = '-9999'
        return fire_info

    def _get_area(self, area=None, SFire_Error=False):
        if area and not SFire_Error: 
            area = float(area)
        elif area and SFire_Error:
            area = float(area)/3.0
        return area

    def get_xwalk_data(self, irow=None, WF_Emission=None, RX_Emission=None, SFire_Error=False):
        FCCS_ID  = irow['fccs_number']
        area     = irow['area']
        fireType = irow['type']

        if not FCCS_ID: print ("invalid FCCS_ID"); return # exit if FCCS_ID is an empty string
        if not area: print ("invalid area"); return # exit if area is an empty string
         
        fireData = dict.fromkeys(self.pollutants)
        area = self._get_area(area, SFire_Error)

        if fireType == 'WF':
            for ikey in fireData.keys():
                fireData[ikey] = self._formatter(area * float(WF_Emission[ikey][FCCS_ID]))
            
            # get virtual heat and area
            conf  = float(WF_Emission['Consumption_Flame'][FCCS_ID])
            virtual_heat_area = self._get_virtual_area_heat(conf, area)
            fireData['ACRESBURNED']  = self._formatter(virtual_heat_area['area'])
            fireData['HFLUX']        = self._formatter(virtual_heat_area['heat'])
    
        elif fireType == 'RX':
            for ikey in fireData.keys():
                fireData[ikey] = self._formatter(area * float(RX_Emission[ikey][FCCS_ID]))
            
            # get virtual heat and area
            conf  = float(RX_Emission['Consumption_Flame'][FCCS_ID])
            virtual_heat_area = self._get_virtual_area_heat(conf, area)
            fireData['ACRESBURNED']  = self._formatter(virtual_heat_area['area'])
            fireData['HFLUX']        = self._formatter(virtual_heat_area['heat'])
        
        # add fire location etc. information 
        fire_info = self._fire_information(irow)
        for ikey in fire_info.keys():
            fireData[ikey] = fire_info[ikey]
        # return the data 
        return fireData

    def get_blueSky_data(self, irow=None, SFire_Error=False):
        fireData = dict.fromkeys(self.pollutants)
        if irow is not None:
            for ikey in fireData.keys():
                 if ikey == 'PM2_5' and irow['pm25']:
                     fireData[ikey] = self._formatter(float(irow['pm25']))
                 elif ikey != 'PM2_5' and irow[ikey.lower()]:
                     fireData[ikey] = self._formatter(float(irow[ikey.lower()]))

            # get virtual heat and area
            if irow['consumption_flaming'] and irow['area']: 
                conf  = float(irow['consumption_flaming'])
                area  = self._get_area(irow['area'], SFire_Error)
                virtual_heat_area = self._get_virtual_area_heat(conf, area)
                fireData['ACRESBURNED']  = self._formatter(virtual_heat_area['area']) 
                fireData['HFLUX']        = self._formatter(virtual_heat_area['heat']) 
            else:
                fireData['ACRESBURNED']  = self._formatter(irow['area']) 
                fireData['HFLUX']        = self._formatter(irow['heat']) 
            
        # add fire location etc. information 
        fire_info = self._fire_information(irow)
        for ikey in fire_info.keys():
            fireData[ikey] = fire_info[ikey]

        #return the dictionary
        return fireData

    def ptday_writer(self, ptday_file=None, country=None, year=None):
        # Create ptday file
        ptday = open(ptday_file,'w')
        ptday.write('#ORL FIREEMIS\n')
        ptday.write('#TYPE    Day-specific Point Source Inventory for FIRES\n')
        ptday.write('#COUNTRY {}\n'.format(country.upper()))
        ptday.write('#YEAR {}\n'.format(year))
        ptday.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
        ptday.write('#DESC FIPS,FIREID,LOCID,SCC,DATA,DATE,DATAVALUE,BEGHOUR,ENDHOUR\n')
        return ptday

    def ptinv_writer(self, ptinv_file=None, country=None, year=None):
        # Create ptinv file
        ptinv = open(ptinv_file,'w')
        ptinv.write('#ORL FIRE\n')
        ptinv.write('#TYPE Point Source Inventory for FIRES\n')
        ptinv.write('#COUNTRY {}\n'.format(country.upper()))
        ptinv.write('#YEAR {}\n'.format(year))
        ptinv.write('#DATA ACRESBURNED HFLUX PM2_5 PM10 CO NH3 NOX SO2 VOC\n')
        ptinv.write('#DESC FIPS,FIREID,LOCID,SCC,NAME,LAT,LON,NFDRSCODE,MATBURNED,HEATCONTENT\n')
        return ptinv
