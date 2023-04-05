# -*- coding: cp936 -*-
import os
import fnmatch
import ee
import urllib.request
import wget

ee.Initialize()
inputdir = "C:\\STAT\\aaa\\"
Out_path = "C:\\STAT\\bbb\\"

def get_property(f,property_name):
    try:
        property_value = f['properties'][property_name]
    except:
            property_value = -9999
    return property_value

pattern = '*.txt'
filenames_all = fnmatch.filter(os.listdir(inputdir), pattern)
for filename in filenames_all:
    txtfilename = inputdir + filename
    tile = filename[:-4]
    try:
        origin_data = ee.ImageCollection('COPERNICUS/S2').filterMetadata('MGRS_TILE', 'equals', tile).filterDate('2015-01-01', '2020-12-31')
        origin_data_size = origin_data.size().getInfo()
        print(tile + ' has ' + str(origin_data_size) + ' images')
        for f in origin_data.getInfo()['features']:
            image_id = f['id']
            fnew = open(Out_path+str(image_id)[14:]+'.txt', 'wb')
            SOLAR_IRRADIANCE_B1 = get_property(f,'SOLAR_IRRADIANCE_B1')
            SOLAR_IRRADIANCE_B2 = get_property(f,'SOLAR_IRRADIANCE_B2')
            SOLAR_IRRADIANCE_B3 = get_property(f,'SOLAR_IRRADIANCE_B3')
            SOLAR_IRRADIANCE_B4 = get_property(f,'SOLAR_IRRADIANCE_B4')
            SOLAR_IRRADIANCE_B5 = get_property(f,'SOLAR_IRRADIANCE_B5')
            SOLAR_IRRADIANCE_B6 = get_property(f,'SOLAR_IRRADIANCE_B6')
            SOLAR_IRRADIANCE_B7 = get_property(f,'SOLAR_IRRADIANCE_B7')
            SOLAR_IRRADIANCE_B8 = get_property(f,'SOLAR_IRRADIANCE_B8')
            SOLAR_IRRADIANCE_B8A = get_property(f,'SOLAR_IRRADIANCE_B8A')
            SOLAR_IRRADIANCE_B9 = get_property(f,'SOLAR_IRRADIANCE_B9')
            SOLAR_IRRADIANCE_B10 = get_property(f,'SOLAR_IRRADIANCE_B10')
            SOLAR_IRRADIANCE_B11 = get_property(f,'SOLAR_IRRADIANCE_B11')
            SOLAR_IRRADIANCE_B12 = get_property(f,'SOLAR_IRRADIANCE_B12')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B1 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B1')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B2 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B2')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B3 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B3')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B4 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B4')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B5 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B5')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B6 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B6')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B7 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B7')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B8 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B9 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B9')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B10 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B10')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B11 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B11')
            MEAN_INCIDENCE_AZIMUTH_ANGLE_B12 = get_property(f,'MEAN_INCIDENCE_AZIMUTH_ANGLE_B12')
            MEAN_INCIDENCE_ZENITH_ANGLE_B1 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B1')
            MEAN_INCIDENCE_ZENITH_ANGLE_B2 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B2')
            MEAN_INCIDENCE_ZENITH_ANGLE_B3 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B3')
            MEAN_INCIDENCE_ZENITH_ANGLE_B4 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B4')
            MEAN_INCIDENCE_ZENITH_ANGLE_B5 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B5')
            MEAN_INCIDENCE_ZENITH_ANGLE_B6 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B6')
            MEAN_INCIDENCE_ZENITH_ANGLE_B7 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B7')
            MEAN_INCIDENCE_ZENITH_ANGLE_B8 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B8')
            MEAN_INCIDENCE_ZENITH_ANGLE_B8A = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B8A')
            MEAN_INCIDENCE_ZENITH_ANGLE_B9 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B9')
            MEAN_INCIDENCE_ZENITH_ANGLE_B10 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B10')
            MEAN_INCIDENCE_ZENITH_ANGLE_B11 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B11')
            MEAN_INCIDENCE_ZENITH_ANGLE_B12 = get_property(f,'MEAN_INCIDENCE_ZENITH_ANGLE_B12')
            REFLECTANCE_CONVERSION_CORRECTION = get_property(f,'REFLECTANCE_CONVERSION_CORRECTION')
            MEAN_SOLAR_AZIMUTH_ANGLE = get_property(f,'MEAN_SOLAR_AZIMUTH_ANGLE')
            MEAN_SOLAR_ZENITH_ANGLE = get_property(f,'MEAN_SOLAR_ZENITH_ANGLE')
            SPACECRAFT_NAME = get_property(f,'SPACECRAFT_NAME')
            string_write = image_id+','+str(SOLAR_IRRADIANCE_B1)+','+str(SOLAR_IRRADIANCE_B2)+','+str(SOLAR_IRRADIANCE_B3) \
                       +','+str(SOLAR_IRRADIANCE_B4)+','+str(SOLAR_IRRADIANCE_B5)+','+str(SOLAR_IRRADIANCE_B6)+','+ \
                       str(SOLAR_IRRADIANCE_B7)+','+str(SOLAR_IRRADIANCE_B8)+','+str(SOLAR_IRRADIANCE_B8A)+','+ \
                       str(SOLAR_IRRADIANCE_B9)+','+str(SOLAR_IRRADIANCE_B10)+','+str(SOLAR_IRRADIANCE_B11)+','+ \
                       str(SOLAR_IRRADIANCE_B12)+','+str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B1)+','+str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B2)+ \
                       ','+str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B3)+','+str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B4)+','+ \
                       str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B5)+','+str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B6)+','+ \
                       str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B7)+','+str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B8)+','+ \
                       str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A)+','+str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B9)+','+ \
                       str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B10)+','+str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B11)+','+ \
                       str(MEAN_INCIDENCE_AZIMUTH_ANGLE_B12)+','+str(MEAN_INCIDENCE_ZENITH_ANGLE_B1)+','+ \
                       str(MEAN_INCIDENCE_ZENITH_ANGLE_B2)+','+str(MEAN_INCIDENCE_ZENITH_ANGLE_B3)+','+ \
                       str(MEAN_INCIDENCE_ZENITH_ANGLE_B4)+','+str(MEAN_INCIDENCE_ZENITH_ANGLE_B5)+','+ \
                       str(MEAN_INCIDENCE_ZENITH_ANGLE_B6)+','+str(MEAN_INCIDENCE_ZENITH_ANGLE_B7)+','+ \
                       str(MEAN_INCIDENCE_ZENITH_ANGLE_B8)+','+str(MEAN_INCIDENCE_ZENITH_ANGLE_B8A)+','+ \
                       str(MEAN_INCIDENCE_ZENITH_ANGLE_B9)+','+str(MEAN_INCIDENCE_ZENITH_ANGLE_B10)+','+ \
                       str(MEAN_INCIDENCE_ZENITH_ANGLE_B11)+','+str(MEAN_INCIDENCE_ZENITH_ANGLE_B12)+','+ \
                       str(MEAN_INCIDENCE_ZENITH_ANGLE_B1)+','+str(REFLECTANCE_CONVERSION_CORRECTION)+','+ \
                       str(MEAN_SOLAR_AZIMUTH_ANGLE)+','+str(MEAN_SOLAR_ZENITH_ANGLE)+','+SPACECRAFT_NAME
            string_write = string_write.encode()
            fnew.write(string_write)
            fnew.close()
            print(image_id)
    except:
        print('Error')
        time.sleep(3)
        ee.Initialize()
    else:
        os.remove(txtfilename)
        print(tile + ' is Ok!')

