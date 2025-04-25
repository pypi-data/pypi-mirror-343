"""
Author: HECE - University of Liege, Pierre Archambeau
Date: 2024

Copyright (c) 2024 University of Liege. All rights reserved.

This script and its content are protected by copyright law. Unauthorized
copying or distribution of this file, via any medium, is strictly prohibited.
"""

from owslib.wms import WebMapService
from PIL import Image
from io import BytesIO
import pyproj
import urllib.parse as ul
import wx
import logging
from typing import Union, Literal
from enum import Enum

from .PyTranslate import _

def to_image(mybytes:BytesIO) -> Image:
    return Image.open(mybytes)

def getWalonmap(cat:Literal['IMAGERIE/ORTHO_2021', 'ALEA', 'CADMAP', 'LIDAXES', '$IDW', 'EAU/ZONES_INONDEES'],
                xl:float,
                yl:float,
                xr:float,
                yr:float,
                w:int = None,
                h:int = None,
                tofile=True) -> BytesIO:

    if cat.find('$')>0:
        catloc=cat[:cat.find('$')]
    elif cat.find('_wo_alea')>0:
        catloc=cat[:cat.find('_wo_alea')]
    else:
        catloc=cat

    try:
        wms=WebMapService('https://geoservices.wallonie.be/arcgis/services/'
                        + catloc+'/MapServer/WMSServer',version='1.3.0')
    except:
        wms=WebMapService('https://eservices.minfin.fgov.be/arcgis/services/'
                        + catloc+'/MapServer/WMSServer',version='1.3.0')
        # wms=WebMapService('http://ccff02.minfin.fgov.be/geoservices/arcgis/services/'
        #                 + catloc+'/MapServer/WMSServer',version='1.3.0')

    ppkm = 300
    if w is None and h is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        w = int(real_w * ppkm)
        h = int(real_h * ppkm)
    elif w is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        ppkm = h/real_h
        w = int(real_w * ppkm)
        # h = int(real_h * ppkm)
    elif h is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        ppkm = w/real_w
        # w = int(real_w * ppkm)
        h = int(real_h * ppkm)

    if tofile:
        img=wms.getmap(layers=['0'],styles=['default'],srs='EPSG:31370',bbox=(xl,yl,xr,yr),size=(w,h),format='image/png',transparent=True)
        out = open('aqualim.png', 'wb')
        out.write(img.read())
        out.close()
        return BytesIO(b'1')
    else:
        mycontents=list(wms.contents)
        curcont=['0']
        curstyles=['default']

        if cat.find('ALEA')>0:
            ech=(xr-xl)/w
            if ech>6.5:
                curcont=['6'] #au-dessus du 1:25000
            else:
                curcont=['5'] #en-dessous du 1:25000 et au-dessus de 1:5000
        elif cat.find('CADMAP')>0:
            curcont=['0,1']
            curstyles=['default,default']
        elif cat.find('LIMITES_ADMINISTRATIVES')>0:
            curcont=['0,1,2,3']
            curstyles=['default,default,default,default']
        elif cat.find('wms')>0:
            curcont=['1,2,3,4,5']
            curstyles=['default,default,default,default,default']
        elif cat.find('LIDAXES')>0:
            curcont=['4,5,6,7,8,9,11,13']
            curstyles=['default,default,default,default,default,default,default,default']
        elif cat.find('IDW')>0:
            curcont=['0']
            curstyles=['default']
        elif cat.find('ZONES_INONDEES')>0:

            if 'wo_alea' in cat:
                curcont = list(wms.contents)[1:]
                curstyles=['default']*len(curcont)
            else:
                curcont = list(wms.contents)
                curstyles=['default']*len(curcont)

        try:
            img=wms.getmap(layers=curcont,styles=curstyles,srs='EPSG:31370',bbox=(xl,yl,xr,yr),size=(w,h),format='image/png',transparent=True)
            return BytesIO(img.read())
        except:
            logging.warning(_('Impossible to get data from web services'))
            pass

def getVlaanderen(cat:Literal['Adpf'],
                xl:float,
                yl:float,
                xr:float,
                yr:float,
                w:int = None,
                h:int = None,
                tofile=True) -> BytesIO:

    catloc=cat

    try:
        wms=WebMapService('https://geo.api.vlaanderen.be/'
                        + catloc+'/wms',version='1.3.0')
    except:
        logging.warning(_('Impossible to get data from web services'))
        return

    ppkm = 300
    if w is None and h is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        w = int(real_w * ppkm)
        h = int(real_h * ppkm)
    elif w is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        ppkm = h/real_h
        w = int(real_w * ppkm)
        # h = int(real_h * ppkm)
    elif h is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        ppkm = w/real_w
        # w = int(real_w * ppkm)
        h = int(real_h * ppkm)

    if tofile:
        img=wms.getmap(layers=['0'],styles=['default'],srs='EPSG:31370',bbox=(xl,yl,xr,yr),size=(w,h),format='image/png',transparent=True)
        out = open('aqualim.png', 'wb')
        out.write(img.read())
        out.close()
        return BytesIO(b'1')
    else:
        mycontents=list(wms.contents)
        curcont=['Adpf']
        curstyles=['default']

        try:
            img=wms.getmap(layers=curcont,styles=curstyles,srs='EPSG:31370',bbox=(xl,yl,xr,yr),size=(w,h),format='image/png',transparent=True)
            return BytesIO(img.read())
        except:
            logging.warning(_('Impossible to get data from web services'))
            pass


def getIGNFrance(cat:str,epsg:str,xl,yl,xr,yr,w,h,tofile=True) -> BytesIO:

    if epsg!='EPSG:4326':
        transf=pyproj.Transformer.from_crs(epsg,'EPSG:4326')
        y1,x1=transf.transform(xl,yl)
        y2,x2=transf.transform(xr,yr)
    else:
        x1=xl
        x2=xr
        y1=yl
        y2=yr

    wms=WebMapService('https://wxs.ign.fr/inspire/inspire/r/wms',version='1.3.0')

    img=wms.getmap(layers=[cat],styles=[''],srs='EPSG:4326',bbox=(x1,y1,x2,y2),size=(w,h),format='image/png',transparent=True)

    if tofile:
        out = open('ignFrance.png', 'wb')
        out.write(img.read())
        out.close()
        return BytesIO(b'1')
    else:
        return BytesIO(img.read())

def getLifeWatch(cat:Literal['None'],
                xl:float,
                yl:float,
                xr:float,
                yr:float,
                w:int = None,
                h:int = None,
                tofile=True,
                format:Literal['image/png', 'image/png; mode=8bit']='image/png') -> BytesIO:

    wms=WebMapService(f'https://maps.elie.ucl.ac.be/cgi-bin/mapserv72?map=/maps_server/lifewatch/mapfiles/LW_Ecotopes/latest/{cat}.map&SERVICE=wms',
                        version='1.3.0')

    ppkm = 300
    if w is None and h is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        w = int(real_w * ppkm)
        h = int(real_h * ppkm)
    elif w is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        ppkm = h/real_h
        w = int(real_w * ppkm)
        # h = int(real_h * ppkm)
    elif h is None:
        real_w = (xr-xl)/1000
        real_h = (yr-yl)/1000
        ppkm = w/real_w
        # w = int(real_w * ppkm)
        h = int(real_h * ppkm)

    MAXSIZE = 2048
    if w > MAXSIZE:
        pond = w / MAXSIZE
        w = MAXSIZE
        h = int(h / pond)
    if h > MAXSIZE:
        pond = h / MAXSIZE
        h = MAXSIZE
        w = int(w / pond)

    if tofile:
        img=wms.getmap(layers=['lc_hr_raster'],
                    #    styles=['default'],
                       srs='EPSG:31370',
                       bbox=(xl,yl,xr,yr),
                       size=(w,h),
                       format='image/png',
                       transparent=False)

        out = open('LifeWatch.png', 'wb')
        out.write(img.read())
        out.close()
        return BytesIO(b'1')
    else:
        mycontents=list(wms.contents)
        curcont=['lc_hr_raster'] # 'MS
        curstyles=['1']

        try:
            img=wms.getmap(layers=curcont,
                        #    styles=curstyles,
                           srs='EPSG:31370',
                           bbox=(xl,yl,xr,yr),
                           size=(w,h),
                           format=format,
                           transparent=False)
            return BytesIO(img.read())
        except:
            logging.warning(_('Impossible to get data from web services'))
            pass

if __name__=='__main__':
    # me=pyproj.CRS.from_epsg(27573)
    # t=pyproj.Transformer.from_crs(27573,4326)
    # getIGNFrance('OI.OrthoimageCoverage.HR','EPSG:27563',878000,332300,879000,333300,1000,1000)
    img = getLifeWatch('',250000,160000,252000,162000,1000,1000,False)
    img = Image.open(img)
    img.show()
    pass