1_Gasflaring_SUM_GEE.py 
This code detects high-temperature anomalies (HTAs) in time-series MSI images of a given tile (e.g. 15RYL), sums all binary images derived from the time-series MSI images (2015-2021), and exports the HTA occurrence images to Google Drive.

2_SEGMENT_GF_CANDIDATES_POLYGON.py
This code segments candidates of offshore GF sites with repeated GFs from the HTA occurrence images using a fixed threshold of four, converts the binary images to vector shapefiles, and then performs a buffer operation. Note that, (1) the above occurrence images include onshore HTAs, false positives, offshore active volanos; (2) the MSI images of a given tile, hosted in the Google Earth Engine, may have several versions due to different processing baselines. False positives must therefore be excluded with the aid of the land boundary mask, the global volcano database, and the global offshore platform inventory.

3_Gasflaring_detection_STAT_GEE.py
Once an offshore GF object (polygon format) is confirmed, this code calculates the time series GF statistics (2015-2021) of the MSI observations in the offshore GF object, including the pixel number of the MSI image, the pixel number of the GF, the reflectance sum of bands 8A, 11, and 12 of the detected GF pixels, the cloud ratio, the satellite name, the acquisition date, and the tile name of the MSI image.

4_CSV2DBF.py
This code converts the CVS files calculated based on the GEE to dbf files.

5_CALCULATE_GF_RADIANCE_PER_OBSERVATION.py
This code calculates the radiance sum of bands 8A, 11, and 12 of the detected GF pixels per MSI observation.

6_MERGE_DBF.py
This code merges all the dbf files into a single file. This file can be further analysed using ArcGIS software.