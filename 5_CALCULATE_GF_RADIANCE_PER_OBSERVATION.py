
import arcpy
from arcpy.sa import *
import os
import fnmatch

arcpy.CheckOutExtension("spatial")


#inputdir and outputdir must be modifed by user
inputdir1="C:\\GF\\GF_STAT_DBF\\"
pattern = '*.dbf'

filenames=fnmatch.filter(os.listdir(inputdir1), pattern)
for filename in filenames:
    try:
        inshape=inputdir1+filename[:-4]+".dbf"
        layername="Layer"+filename[:-4]
        arcpy.AddField_management(inshape, "YEAR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(inshape, "YEAR", "Left( [s2_date],4 )", "VB", "")
        arcpy.AddField_management(inshape, "IDD_YEAR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(inshape, "IDD_YEAR", "[IDD] &\"_\"& [YEAR]", "VB", "")
        
        arcpy.AddField_management(inshape, "R8A_SUM", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(inshape, "R8A_SUM", "[RCC] * [B8A_sum] /10000 * [SI_B8A] *Cos ( [MSZA] *3.1415926 / 180.0 )/3.1415926", "VB", "")
        arcpy.AddField_management(inshape, "R11_SUM", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(inshape, "R11_SUM", "[RCC] * [B11_sum] /10000 * [SI_B11] *Cos ( [MSZA] *3.1415926 / 180.0 )/3.1415926", "VB", "")
        arcpy.AddField_management(inshape, "R12_SUM", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(inshape, "R12_SUM", "[RCC] * [B12_sum] /10000 * [SI_B12] *Cos ( [MSZA] *3.1415926 / 180.0 )/3.1415926", "VB", "")
        arcpy.AddField_management(inshape, "DETECTED", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        
    except:
        print(filename+" is failed!")
    else:
        print(filename + " is ok!")
