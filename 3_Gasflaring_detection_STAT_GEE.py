import ee
import os
import fnmatch
import shapefile
import pandas as pd
import datetime
import math
ee.Initialize()


date1 = ee.Date('2015-01-01')
date2 = ee.Date('2021-12-31')


def get_data_property(image):
    return ee.Feature(None, {
        'id': image.get('system:index'),
        'date': ee.Date(image.get('system:time_start')).format("yyyy-MM-dd"),
        's2_name': image.get('SPACECRAFT_NAME'),
        'tile_name': image.get('MGRS_TILE')})


def list_to_collection(id_list, geometry):
    new_list = []
    for id in id_list:
        new_list.append(ee.Image('COPERNICUS/S2/'+id).clip(geometry))
    new_col = ee.ImageCollection(new_list)
    return new_col


def gas_flaring(image):
    # read the MSI image bands
    b8a = image.select('B8A')
    b11 = image.select('B11')
    b12 = image.select('B12')
    qa = image.select('QA60')

    ## read the MSI image properties]
    #RCC = ee.Number(image.get('REFLECTANCE_CONVERSION_CORRECTION'))
    #SI_B8A = ee.Number(image.get('SOLAR_IRRADIANCE_B8A'))
    #SI_B11 = ee.Number(image.get('SOLAR_IRRADIANCE_B11'))
    #SI_B12 = ee.Number(image.get('SOLAR_IRRADIANCE_B12'))
    #MSZA = ee.Number(image.get('MEAN_SOLAR_ZENITH_ANGLE'))

    ## calculate the band radiance; these online calculations are differ to those calculated offline
    #cos_MSZA = (MSZA.multiply(ee.Number(3.1415926)).divide(ee.Number(180.0))).cos()
    #b8a_multiplier = RCC.multiply(SI_B8A).multiply(cos_MSZA).divide(ee.Number(31415.926))
    #b11_multiplier = RCC.multiply(SI_B11).multiply(cos_MSZA).divide(ee.Number(31415.926))
    #b12_multiplier = RCC.multiply(SI_B12).multiply(cos_MSZA).divide(ee.Number(31415.926))
    #r_b8a = b8a.multiply(b8a_multiplier).toFloat()
    #r_b11 = b8a.multiply(b11_multiplier).toFloat()
    #r_b12 = b8a.multiply(b12_multiplier).toFloat()

    # detect high-temperature anomalies from the MSI image
    a = ((b12.subtract(b11)).divide(b8a)).gte(0.3)
    b = b8a.gt(50)
    c = b11.gt(50)
    d = b12.gte(200)
    abcd = (a.add(b).add(c).add(d)).eq(4)

    e = b11.gt(10000)
    f = b12.gt(10000)
    ef = (e.add(f)).eq(2)
    bin1 = (abcd.add(ef)).gte(1)
    bin1 = bin1.rename('gf_result')

    # generate a binary extent image of MSI observation
    g = b8a.gt(0)
    h = b11.gt(0)
    i = b12.gt(0)
    bin2 = (g.add(h).add(i)).eq(3)
    bin2 = bin2.rename('data_result')

    # generate reflectance images of GF pixels
    b8a_new = b8a.multiply(bin1)
    b11_new = b11.multiply(bin1)
    b12_new = b12.multiply(bin1)
    b8a_new = b8a_new.rename('b8a_new')
    b11_new = b11_new.rename('b11_new')
    b12_new = b12_new.rename('b12_new')

    # generate a binary image of clouds
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0)
    mask1 = qa.bitwiseAnd(cirrusBitMask).eq(0)
    cloud = (mask.add(mask1)).eq(2)
    cloud = cloud.rename('cloud')

    return image.addBands([bin1,bin2,b8a_new,b11_new,b12_new,cloud])
    #return image.addBands([bin1,bin2,b8a_new,b11_new,b12_new,r_b8a_new,r_b11_new,r_b12_new,cloud])

inputdir = "C:\\GF\\GF_object\\"
filenames = fnmatch.filter(os.listdir(inputdir), "*.shp")

for filename in filenames:
    in_shp = os.path.join(inputdir, filename)
    border_shape = shapefile.Reader(in_shp)
    border = border_shape.shapes()

    for b in border:
        time1 = datetime.datetime.now()
        border_points = b.points
        border_points = [list(b_p) for b_p in border_points]
        
        geometry = ee.Geometry.Polygon(border_points)
        origin_data = ee.ImageCollection('COPERNICUS/S2').filterBounds(geometry).filterDate(date1, date2)
        origin_data_size = origin_data.size().getInfo()
        
        if origin_data_size > 0:
            data_property = origin_data.map(get_data_property)
            data_id = data_property.aggregate_array('id').getInfo()
            data_date = data_property.aggregate_array('date').getInfo()
            data_s2_name = data_property.aggregate_array('s2_name').getInfo()
            data_tile_name = data_property.aggregate_array('tile_name').getInfo()
            
            df = pd.DataFrame({'id':data_id,'date':data_date,'s2_name':data_s2_name,'tile_name':data_tile_name})
            df_grouped = df.groupby(df['date'])
            count = 0
            data_size,detect_size,B8A_sum,B11_sum,B12_sum,cloud_ratio,s2_name,s2_date,tile_name,RCC,SI_B8A,SI_B11,SI_B12,MSZA = [
                [] for t in range(14)]
            out_name = os.path.join(inputdir, filename.replace('.shp','.csv'))
            
            for i,j in df_grouped:
                count += 1
                id_list = j['id'].tolist()
                date_list = j['date'].tolist()
                s2_name_list = j['s2_name'].tolist()
                tile_name_list = j['tile_name'].tolist()
                print(count, date_list)
                new_col = list_to_collection(id_list, geometry)

                info = new_col.first().getInfo()['properties']
                RCC_i = info['REFLECTANCE_CONVERSION_CORRECTION']
                SI_B8A_i = info['SOLAR_IRRADIANCE_B8A']
                SI_B11_i = info['SOLAR_IRRADIANCE_B11']
                SI_B12_i = info['SOLAR_IRRADIANCE_B12']
                MSZA_i = info['MEAN_SOLAR_ZENITH_ANGLE']
                RCC.append(RCC_i)
                SI_B8A.append(SI_B8A_i)
                SI_B11.append(SI_B11_i)
                SI_B12.append(SI_B12_i)
                MSZA.append(MSZA_i)

                new_col = new_col.map(gas_flaring)
                new_col_1 = ee.ImageCollection(new_col.select(
                    ['data_result', 'gf_result', 'b8a_new', 'b11_new', 'b12_new', 'cloud']))
                mosaic = ee.Image(new_col.max()).clip(geometry)
                sumDictionary = mosaic.reduceRegion(ee.Reducer.sum(), geometry, 20)
                
                data_size_i = sumDictionary.getNumber('data_result').getInfo()
                detect_size_i = sumDictionary.getNumber('gf_result').getInfo()
                B8A_sum_i = sumDictionary.getNumber('b8a_new').getInfo()
                B11_sum_i = sumDictionary.getNumber('b11_new').getInfo()
                B12_sum_i = sumDictionary.getNumber('b12_new').getInfo()
                cloud_sum_i = sumDictionary.getNumber('cloud').getInfo()
                data_size.append(data_size_i)
                detect_size.append(detect_size_i)
                B8A_sum.append(B8A_sum_i)
                B11_sum.append(B11_sum_i)
                B12_sum.append(B12_sum_i)

                if data_size_i == 0:
                    cloud_ratio_i = 0
                else:
                    cloud_ratio_i = 100 - cloud_sum_i / data_size_i * 100
                cloud_ratio.append(cloud_ratio_i)
                s2_name.append(s2_name_list[0])
                s2_date.append(date_list[0])
                tile_name.append(tile_name_list[0])

            df_new = pd.DataFrame({'data_size': data_size,
                                   'detect_size': detect_size,
                                   'B8A_sum': B8A_sum,
                                   'B11_sum': B11_sum,
                                   'B12_sum': B12_sum,
                                   'cloud_ratio': cloud_ratio,
                                   's2_name': s2_name,
                                   's2_date': s2_date,
                                   'tile_name': tile_name,
                                   'RCC': RCC,
                                   'SI_B8A': SI_B8A,
                                   'SI_B11': SI_B11,
                                   'SI_B12': SI_B12,
                                   'MSZA': MSZA,})
            df_new.to_csv(out_name, mode = 'a', sep=',', index=False)
            print("OK!")
