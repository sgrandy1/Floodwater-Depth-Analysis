# RI-Floodwater-Depth-Tools
*Python Toolbox for Floodwater Depth Analysis of Rhode Island Coast*

Author: Sean Grandy, 4/30/2019

All tools released under MIT license, and no warranty is implied

### Background Information
This repository contains tools that can be used to calculate floodwater depth of 100 year floods along the Rhode Island coast and additional feet of flooding from a given sea level rise scenario. The tools produce two water depth raster datasets:

**FEMA Water Depth:** Based on FEMA BFE (base flood elevation) from FEMA Flood Hazards data and ground elevation data from an input DEM.

**Depth Difference:** Based on FEMA floodwater depth output and input floodwater depth from a given sea level rise scenario. Floodwater depth for various sea level rise (SLR) scenarios were created by the [Coastal Resources Center](https://crc-uri.maps.arcgis.com/apps/MapSeries/index.html?appid=3ba5c4d9c0744392bec2f4afb6ee2286) for their [STORMTOOLS](https://crc-uri.maps.arcgis.com/home/item.html?id=660713aa75c64d54bd48c6d0014b26a9) web map application. The CRC floodwater depth is based on new BFE data they calculated through STORMTOOL models, referred to as "Suggested Design Elevation" (SDE) to avoid confusion with existing FEMA BFE maps. Sea Level Rise scenarios of 2, 3, 5, 7, and 10 feet were caclulated as part of their analysis.

FEMA flood zone data has important implications, especially in regard to flood insurance rates. The FEMA water depth data supplements this data by indicating how much inundatation from floodwaters would occcur at any particular location within the area of interest. The depth difference layer further supplements this by predicting how much more inundation could occur at that particular location given a certain sea level rise scenario. 

### Tool Descriptions 
The three tools are presented in the toolbox as three parts of the overall analysis: a projection and clip of the FEMA Flood Hazard Zones data to an area of interest, the conversion of this output to a BFE raster dataset, and two raster calculations to determine FEMA water depth and depth difference. Specific details for each tool are noted below:

* Step 1: FEMA AOI Clip
  * This tool projects the FEMA Flood Hazards feature class for Rhode Island into Rhode Island State Plane Feet. The projected feature class is then clipped to the input area of interest boundaries. 
* Step 2: FEMA BFE
  * This tool takes the FEMA area of interest clip output from Step 1 and converts the feature class into a base flood elevation raster dataset based on the attribute 'STATIC_BFE'. This raster dataset is then reclassified to remove areas that do not undergo flooding. *NOTE:* FEMA BFE raster dataset that is created has a pixel size of 30.
* Step 3: Depth and Depth Diff
  * This tool uses the FEMA Base Flood Elevation raster dataset from Step 2 to produce two floodwater depth raster datasets. The first raster dataset showcases floodwater depth based on the difference of FEMA BFE and the input DEM raster. The second raster dataset showcases additional floodwater depth from a given sea level rise scenario based on the difference of the input sea level rise floodwater depth and the FEMA floodwater depth output. *NOTE:* input raster datasets should have a pixel size of 30 to undergo raster calculations with FEMA BFE from Step 2.

**Important Note:** The tools included in this toolbox are modified to work with the sample data included in the repository. The SLR water depth included in the sample data has been resampled to a smaller data size (from a 3.2808 pixel size 30 pixel size) to more easily demo the tools in the toolbox. Because all CRC sea level rise depth data is originally in a 3.2808 pixel size, when conducting the depth analyses, the script should be modified to create a raster in this pixel size and the input raster elevation data should be in this pixel size as well.

**Sample data included:** FEMA_Flood_Hazard_Areas.shp, South_Kingstown_Boundary.shp, skdem, slr3_depth

*All data is from RIGIS excluding slr3_depth which is from URI CRC*

