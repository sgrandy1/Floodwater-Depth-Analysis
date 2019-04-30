# RI-Floodwater-Depth-Tools
*Python Toolbox for Floodwater Depth Analysis of Rhode Island Coast*

### Background Information
This repository contains tools that can be used to calculate floodwater depth of 100 year floods along the Rhode Island coast and additional feet of flooding from a given sea level rise scenario. The tools produce two water depth raster datasets:

**FEMA Water Depth:** Based on FEMA BFE (base flood elevation) from FEMA Flood Hazards data and ground elevation data from an input DEM.

**Depth Difference:** Based on FEMA floodwater depth output and input floodwater depth from a given sea level rise scenario. Floodwater depth for various sea level rise scenarios were created by the Coastal Resources Center for their STORMTOOLS web map application. The CRC floodwater depth is based on new BFE data they calculated through STORMTOOL models, referred to as "Suggested Design Elevation" (SDE) to avoid confusion with existing FEMA BFE maps. Sea Level Rise scenarios of 2, 3, 5, 7, and 10 feet were caclulated as part of their analysis.

FEMA flood zone data has important implications, especially in regard to flood insurance rates. The FEMA water depth data supplements this data by indicating how much inundatation from floodwaters would occcur at any particular location within the area of interest. The depth difference layer further supplements this by predicting how much more inundation could occur at that particular location given a certain sea level rise scenario. 

### Tool Descriptions 
The three tools are presented in the toolbox as three parts of the overall analysis: a projection and clip of the FEMA Flood Hazard Zones data to an area of interest, the conversion of this output to a BFE raster dataset, and two raster calculations to determine FEMA water depth and depth difference. Specific details for each tool are noted below:

*Step 1: FEMA AOI Clip
  *"This tool projects the FEMA Flood Hazards feature class for Rhode Island into Rhode Island State Plane Feet. The projected feature class is then clipped to the input area of interest boundaries."


