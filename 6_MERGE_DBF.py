import arcpy
import os
import fnmatch

arcpy.CheckOutExtension("spatial")
arcpy.env.extent = "MAXOF"
arcpy.env.overwriteOutput = True

# inputdir and outputdir must be modifed by user
inputdir = "C:\\GF\\GF_STAT_DBF\\"
outputfile = "C:\\GF\\GF_MERGE_ALL.dbf"

#arcpy.env.outputCoordinateSystem = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
#arcpy.env.extent = "-180 -89 180 89"
#arcpy.env.geographicTransformations = ""

pattern = "*.dbf"
filenames = fnmatch.filter(os.listdir(inputdir), pattern)
for filename in filenames:
    inputfile += "\"" + inputdir + foldername + "\\" + filename + "\"" + ";"
arcpy.Merge_management(inputfile, outputfile)
print outputfile + " has been finished!"
