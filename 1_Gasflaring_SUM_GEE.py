import ee
import pandas as pd
# import urllib.request
import datetime
import os
import fnmatch
import time
ee.Initialize()

tile = ["14QQH","14QRF","14QRG"]
# tile = ["14QQH","14QRF","14QRG","14QRH","14RPP","14RQP","14RQQ","14RQR","14RQS","14RRP","15QTA","15QTB","15QTC","15QUA","15QUB","15QUC","15QVA","15QVB","15QVC","15QWA","15QWB","15QWC","15QXA","15QXB","15QXC","15QYB","15QYC","15RTJ","15RTK","15RTL","15RTM","15RTN","15RUJ","15RUK","15RUL","15RUM","15RUN","15RVJ","15RVK","15RVL","15RVM","15RVN","15RWJ","15RWK","15RWL","15RWM","15RWN","15RXJ","15RXK","15RXL","15RXM","15RXN","15RYJ","15RYK","15RYL","15RYM","15RYN","15RYP","15RZJ","16RBP","16RBQ","16RBR","16RBS","16RBT","16RBU","16RCP","16RCQ","16RCR","16RCS","16RCT","16RCU","16RDP","16RDQ","16RDR","16RDS","16RDT","16RDU"]
date1 = ee.Date('2015-01-01')
date2 = ee.Date('2021-12-31')


def get_data_property(image):
    return ee.Feature(None, {
        'id': image.get('system:index'),
        'date': ee.Date(image.get('system:time_start')).format("yyyy-MM-dd")})


def list_to_collection(id_list):
    new_list = []
    for id in id_list:
        new_list.append(ee.Image('COPERNICUS/S2/'+id))
    new_col = ee.ImageCollection(new_list)
    return new_col


def gas_flaring(image):
    b8a = image.select('B8A')
    b11 = image.select('B11')
    b12 = image.select('B12')
    
    a = ((b12.subtract(b11)).divide(b8a)).gte(0.3)
    b = b8a.gt(50)
    c = b11.gt(50)
    d = b12.gte(200)
    abcd = (a.add(b).add(c).add(d)).eq(4)

    
    e = b11.gt(10000)
    f = b12.gt(10000)
    ef = (e.add(f)).eq(2)
    
    result = (abcd.add(ef)).gte(1)
    result = result.rename('gf_result')
    return result


for p in tile:

    time1 = datetime.datetime.now()

    try:
        origin_data = ee.ImageCollection('COPERNICUS/S2').filterMetadata('MGRS_TILE','equals',p).filterDate(date1, date2)
        origin_data_size = origin_data.size().getInfo()
        print(origin_data_size)

        if origin_data_size == 0:
            print(p + ' has none data.')
        else:
            data_property = origin_data.map(get_data_property)
            data_id = data_property.aggregate_array('id').getInfo()
            data_date = data_property.aggregate_array('date').getInfo()
            df = pd.DataFrame({'id':data_id,'date':data_date})
            df_grouped = df.groupby(df['date'])
            new_data_list = []
            count = 0
            for i,j in df_grouped:
                count += 1
                id_list = j['id'].tolist()
                date_list = j['date'].tolist()
                print(count, date_list)

                new_col = list_to_collection(id_list)
                new_col = new_col.map(gas_flaring)
                geometry1 = new_col.geometry().getInfo()
                mosaic = ee.Image(new_col.max()).clip(geometry1)
                new_data_list.append(mosaic)

            new_data = ee.ImageCollection(ee.List(new_data_list))
            new_data_size = new_data.size().getInfo()
            print('Mosaic '+str(origin_data_size)+' images to '+str(new_data_size)+' images.')

            geometry = new_data.geometry().getInfo()
            result_sum = ee.Image(new_data.sum().toUint8()).clip(geometry)

            task_config = {
                'folder': 'Gasflaring',
                'scale': 20,
                'region': new_data.geometry(),
                'maxPixels': 1e13
                }
            task = ee.batch.Export.image(result_sum, p + '_sum', task_config)
            task.start()
            print(p + ' is finished!')

            time2 = datetime.datetime.now()
            timedelta = (time2 - time1).total_seconds()
            print("duration:" + str(timedelta) + "s!")

    except:
        print('Error')
        time.sleep(10)
        ee.Initialize()