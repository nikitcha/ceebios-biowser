import numpy
import cv2
import os
import zipfile
from PIL import Image
import io
import requests
import pandas

fpre = 'wc2.1_10m_'
climate_dict = {
    'Elevation':'elev',
    'Precip.':'prec',
    'Solar Rad.':'srad',
    'Temp. Avg.':'tavg',
    'Temp. Min':'tmin',
    'Temp. Max.':'tmax',
    'Pressure':'vapr',
    'Wind':'wind',
    }

res_dict = {512:'@1x.png', 1024:'@2x.png', 2048:'@3x.png', 4096:'@4x.png'}
mapi_api = "https://api.gbif.org/v2/map/occurrence/density/0/"
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def clean_data(data, src):
    if src=='Elevation':
        data[data<0] = 0
    if src=='Precip.':
        data[data<0] = 0
    if src=='Solar Rad.':
        data[data==numpy.max(data)] = 0
    if 'Temp' in src:
        data[data==numpy.min(data)] = 0
    if src=='Pressure':
        data[data<0] = 0
    if src=='Wind':
        data[data<0] = 0
    return data


def get_climate_data(src='Elevation'):
    zip_file = os.path.join('climate', fpre+climate_dict[src])+'.zip'
    data = []
    with zipfile.ZipFile(zip_file) as z:
        for filename in z.namelist():
            if '.tif' in filename:
                # read the file
                with z.open(filename) as f:
                    im = Image.open(f)
                    data.append(numpy.array(im))
    data = numpy.stack(data,axis=2)
    data = clean_data(data, src)
    return data

def make_url(x, taxon, res=1024):
    url = "{x}/0{res}?srs=EPSG:4326&bin=square&squareSize=16&taxonKey={taxon}&style=classic-noborder.poly".format(x=x, res=res_dict[res],taxon=str(taxon))
    return mapi_api+url

def get_taxon_distribution(taxon, res=1024):
    img = []
    for x in range(2):
        response = requests.get(make_url(x, taxon, res))
        try:
            i = Image.open(io.BytesIO(response.content))
            img.append(numpy.array(i))
        except:
            img.append(numpy.zeros((res,res,4)))
    img = numpy.concatenate(img,axis=1)/255
    distribution = (img[:,:,0] + 1-img[:,:,1])*img[:,:,3]
    return distribution

def calc_stat(src, distribution):
    _data = numpy.load('./climate/'+climate_dict[src]+'.npy')
    distribution[distribution==0] = numpy.nan
    stat = _data*distribution[:,:,None]
    vstat = numpy.reshape(stat, -1)
    vstat = vstat[numpy.isfinite(vstat)]
    ptiles = [0.1,25,50,75,99.9]
    aggstat = {}
    if stat.shape[-1]==12:
        for i in range(stat.shape[-1]):
            vstat = numpy.reshape(stat[:,:,i], -1,)
            vstat = vstat[numpy.isfinite(vstat)]
            aggstat.update({months[i]:[numpy.percentile(vstat,p) for p in ptiles]})
    else:
        vstat = numpy.reshape(stat[:,:,0], -1,)
        vstat = vstat[numpy.isfinite(vstat)]
        aggstat = {'Elevation':[numpy.percentile(vstat, p) for p in ptiles]}
    return pandas.DataFrame.from_dict(aggstat), vstat

def preprocess_climate_data(shape=(2048,1024)):
    for k in list(climate_dict.keys()):
        data = get_climate_data(k)
        maxint = 32767
        mindata = numpy.min(data)
        maxdata = numpy.max(data)
        scaled = (data-mindata)/(maxdata-mindata)*maxint
        resized = cv2.resize(scaled.astype('int16'), shape, interpolation= cv2.INTER_LINEAR)
        _data = resized/maxint*(maxdata-mindata)+mindata
        _data = numpy.atleast_3d(_data)
        print(_data.shape)
        numpy.save('./climate/'+climate_dict[k], _data)

