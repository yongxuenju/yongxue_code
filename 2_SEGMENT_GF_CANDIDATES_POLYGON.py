# -*- coding: cp936 -*-
import arcpy
from arcpy.sa import *
import os
import fnmatch

arcpy.CheckOutExtension("spatial")
arcpy.env.extent = "MAXOF"
arcpy.env.overwriteOutput = True

inputdir="C:\\GF\\SUM\\"
outputdir="C:\\GF\\GF_CANDIDATES\\"
outputdir1="C:\\GF\\GF_CANDIDATES_BUFFER\\"
pattern = '*.tif'

filenames=fnmatch.filter(os.listdir(inputdir), pattern)
for filename in filenames:
    try:
        BIN=Raster(inputdir+filename)
        BIN1=Con(BIN>=4, 1)
        SHPfilename=outputdir+filename[:-4]+".shp"
        arcpy.RasterToPolygon_conversion(BIN1, SHPfilename, "NO_SIMPLIFY", "Value")
        neighborhood = NbrCircle(30, "CELL")
        OUTputfile=outputdir1+filename[:-4]+".shp"
        arcpy.Buffer_analysis(SHPfilename, OUTputfile2, "20 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
        arcpy.AddField_management(OUTputfile2, "ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(OUTputfile2, "ID", "[FID]", "VB", "")
    except:
        print(filename)
    else:
        print('OK')
